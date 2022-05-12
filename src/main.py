import xarray as xr
import os
import xesmf as xe
import numpy as np
import pickle
import pandas as pd

os.environ['HDF5_USE_FILE_LOCKING']='FALSE'

dataDIR_1 = './data/sea_ice_thickness/*.nc'
dataDIR_2 = './data/sst/new_sst/*.nc'

def process_data_from_netCDF():
    ds = xr.open_mfdataset(dataDIR_1)
    ds_sst = xr.open_mfdataset(dataDIR_2)


    print(ds_sst)

    


    sq_ds_sst = ds_sst.sel(lat=slice(43, 89))
    small_sst = sq_ds_sst.drop_dims("field_name_length").drop_dims("fields").drop_dims("fieldsp1")
    

    df_thickness = ds.to_dataframe().dropna()


    thickness_times = []
    for i in df_thickness.index:
        thickness_times.append(i[2])


    # print(df_thickness.index[2])
    #we now have something to index by, the new df will have lat, long, time as indices
    #and thickness as a column
    #this will best match the sst dataset
    # print(thickness_times)
    # print(len(thickness_times))

    #pieces of data needed:
        #lat -> df_thickness['lat']
        #lon -> df_thickness['lon']
        #time -> thickness_times    WHY CANT WE USE TIME_BNDS AGAIN?
        #thickness -> df_thickness['sea_ice_thickness'].to_numpy()

    np_thickness_small = 8


    indices = create_multi_index(df_thickness['lat'], df_thickness['lon'], thickness_times)

    df_thickness_small = pd.DataFrame(df_thickness['sea_ice_thickness'].to_numpy(), index=indices, columns=['sea_ice_thickness']).drop_duplicates()
    df_thickness_small.index.names = ['time', 'lat', 'lon']



    # print("THICKNESS LAT AND LON VALUES")
    # print(df_thickness_small.index)
    # print(df_thickness_small)
    # print(df_thickness['lon'].shape)

 

    # np_t_small = np.column_stack([df_thickness['lat'], df_thickness['lon'], thickness_times])
    # np_t_small = [df_thickness['lat'], df_thickness['lon'], thickness_times]
    
    # df_t_small = pd.DataFrame(index=np_t_small)
    # print(df_t_small.index)
    # print(df_t_small.columns)

    # converted_ds_thickness = pd.DataFrame(df_t_small, columns=['lat', 'lon', 'sea_ice_thickness'])

    df_sst = small_sst.to_dataframe().dropna()

    print(df_sst)


    converted_ds_sst = xr.Dataset.from_dataframe(df_sst)
    # print(converted_ds_sst)
    # print(converted_ds_sst['lat']) #this is how you extract lat/lon for the sst set
    # print(small_sst['lat'].values.max())
    # print("LOOKIE HERE")
    # print(np.amax(ds['lat'].values))
    # print(len(df_thickness['lat']))
    # print(df_thickness['lat'].max())
    # print(df_thickness['lat'].min())

    converted_ds_thickness = xr.Dataset.from_dataframe(df_thickness_small)


    return converted_ds_sst, converted_ds_thickness



def create_multi_index(lat, lon, time):
    arrays = [time, lat, lon]
    tuples = list(zip(*arrays))
    index = pd.MultiIndex.from_tuples(tuples, names=["time", "lat", "lon"])
    # print(tuples)
    # return index
    return index


def build_regridder_sst(ds_sst):
    ds_out = xr.Dataset(
        {
            "lat": (["lat"], np.arange(67.323830, 81.639655, 0.07)),  #lat will increment by 0.070000
            "lon": (["lon"], np.arange(-179.648496, 179.644130, 0.1)), #lon will increment by 0.01??
        }
    )

    regridder = xe.Regridder(ds_sst, ds_out, "bilinear")

    return regridder

def build_regridder_thickness(ds_thickness):
    #this regridder will be based on numpy arrays


    # grid_in = {"lat": , "lon", }
    # grid_out = {
    #     "lat": np.arange()
    #     "lon": np.arange()
    # }

    pass

def test_np_regrid():

    fake_lat = [0, 1, 2, 3, 4, 5]
    fake_lon = [4, 5, 6, 7, 8, 9]

    fake_lat_out = [0.1, 0.2, 0.3]
    fake_lon_out = [1, 2, 3]

    fake_time = [13, 14, 15, 16, 17]
    fake_thickness = [0.124, 0.234, 0.346, 0.124, 0.235]

    grid_in = {"lon": fake_lon, "lat": fake_lat}

    grid_out = {
        "lon": fake_lon_out,
        "lat": fake_lat_out,
    }

    regridder = xe.Regridder(grid_in, grid_out, "bilinear")

    np_t_small = np.column_stack([fake_lon, fake_lat])
    print(np_t_small)
    print(np_t_small.shape)

    data_out = regridder(np_t_small)
    data_out.shape




    # ds_out = xr.Dataset(
    #     {
    #         "lat": (["lat"], np.arange(67.323830, 81.639655, 0.07)),  #lat will increment by 0.070000
    #         "lon": (["lon"], np.arange(-179.648496, 179.644130, 0.1)), #lon will increment by 0.01??
    #     }
    # )

    # regridder = xe.Regridder(ds_thickness, ds_out, "bilinear")

    # return regridder

def regrid_sst_data(ds_sst, regridder):
    ds_sst_out = regridder(ds_sst)
    regrid_df_sst = ds_sst_out.to_dataframe()

    regrid_df_sst.to_pickle("./Regrid_SST_Data.pkl")


def regrid_thickness_data(ds_thickness, regridder):
    #we are regridding using a numpy array instead of a dataset
    #bc the converted dataset for ice thickness is too large

    ds_thickness_out = regridder(ds_thickness)
    regrid_df_thickness = ds_thickness_out.to_dataframe()

    regrid_df_thickness.to_pickle("./RegridThickness_Data.pkl")


def main():
    print("Hello World!")

if __name__ == "__main__":
    converted_ds_sst, converted_ds_thickness = process_data_from_netCDF()

    # print("data processed")
    # # regridder = build_regridder_sst(converted_ds_sst)
    # regridder = build_regridder_thickness(converted_ds_thickness)
    # print("regridder built")
    # # regrid_sst_data(converted_ds_sst, regridder)
    # regrid_thickness_data(converted_ds_thickness, regridder)

    # print("DONE")

    # test_np_regrid()
