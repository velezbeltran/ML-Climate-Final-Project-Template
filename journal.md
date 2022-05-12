First Update (Week 7):

I apologize that it has taken so long for me to update. A huge blocker for me these past few weeks has been finding a proper dataset or even any prior work regarding the topic that I was initially interested in pursuing (finding ways to track carbon emissions or detect ocean waste resulting from the production of fast fashion). After discussing with Professor Kucukelbir, I decided it was best to move to another subject and seek out papers which had associated code from workshop papers to see where I might be able to get a little bit of a start. 

I found an interesting paper regarding hurricane forcasting in 2021 Climate Change AI workshop papers and was able to find their source code and data set. This paper details a multimodal framework utilizing novel feature extraction as well as different ensemble methods to maximize performance. Not only are there many different aspects of ML being combined here, but it is mentioned that the authors believe this can be generalized to other satellite imagery datasets. I believe this will be a good place to start to see what other optimizations are able to be made, or even if there might be other datasets for which the novel feature extraction methodlogies can be applied. 


Update :
Something that is particularly interesting to me as I am doing a deeper dive into the paper is the concept of reanalysis maps. This video is a particularly helpful resource that I found: https://www.youtube.com/watch?v=FAGobvUGl24

Since the scope of the paper I mentioned above is a little bit wide for me, so for now I may focus on reanalysis maps. From a quick literature review, the ERA5 dataset seems to be what is used for many such projects. I will link it here for ease of access: https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era5

Digging deeper into the source of the ERA5 dataset, I also stumbled upon a dataset for sea ice thickness in the arctic which intrigued me. Although very different from hurricane forecasting, I did a little bit of side research about sea ice and its role in climate change. Here is a link for my future reference: https://oceanservice.noaa.gov/facts/sea-ice-climate.html#:~:text=Changes%20in%20the%20amount%20of,to%20climate%20change%20on%20Earth.

I am now wondering whether it might be interesting to instead examine possible correlations of sea ice thickness with ocean temperatures/sea surface temperature. I will link the sea ice dataset information here: https://cds.climate.copernicus.eu/cdsapp#!/dataset/satellite-sea-ice-thickness?tab=overview


Update:

I have been trying to extract the data but it is in the form of NetCDF files which I am unfamiliar with. I have found this link that might be able to help me extract some information and understand the raw data using Python: https://www.youtube.com/watch?v=VH-PCQ991fw


I am currently facing confusion over the representation of longitude and latitude, which seem to represented using 2d coordinates. However, in the given array representing sea ice thickness, only three coordinates are given: time, lat, long. So I am having trouble reconciling why it seems lat/lon are represented using 2 dimensions in one form and 1 dimension in another. Here is a link that offers more explanation about why this might be: https://stackoverflow.com/questions/63169963/why-latitudes-and-longitudes-are-two-dimensional-arrays-in-netcdf-file#:~:text=The%20latitude%20and%20longitude%20coordinates,use%20of%20the%20coordinates%20attribute.

So it turns out I think I am just not that familiar with gridded data. The lat and lon coordinates are coded with 2 dimensions for each space in the grid. For now, I will format the data in a csv with latitude, longitude, time (units are seconds after a certain date) and sea ice thickness (in m).


I know there are definitely datasets out there which document sea surface temperature across longitude and latitude, but I am worried about being able to easily find a dataset for which I will be able to match the latitudes and longitudes to be able to find the accurate sea surface temperatures for the corresponding sea ice thicknesses. After doing some research to see how other people might be solving this issue, I came across this post which has definitely piqued my interest: https://stackoverflow.com/questions/46882274/fuzzy-merging-two-data-sets-by-lat-lon-and-time

I wonder if a portion of this project can be focused on the best distance metric to be able to mesh together the two datasets that I am interested in. Another challenge is that that the sea ice data is gathered in monthly increments while the sea temperature data was taken daily. I will link the sea surface temperature dataset that I am currently eyeing here: https://cds.climate.copernicus.eu/cdsapp#!/dataset/satellite-sea-surface-temperature-ensemble-product?tab=overview


I wrote some python code to extract the necessary information from the sea ice thickness dataset to extract time, lat, long, and thickness. This turns out to be over 100,000 data points for each time stamp and with all the data available from the dataset, this exceeds the amount of rows in an excel column. I will try to extract less data for the set I'm looking to combine with the sea surface temperatures. Since the range of availability for the thickness dataset ranges from 2002-2022 and the sea surface temperature ranges only from 1981-2016. I will therefore try only extracting from 2022-2016 for both datasets to maximize compatibility.

So as it turns, out there seems to be a much easier eay to maniputlate and extract netcdf data using the xarray library. This was very simple to use on the thickness data as each measurement is only 432x432. However, when trying to open even 1 of the sea surface temperature files, Google Colab (which is what I'm using to test snippets of code for the time being) runs out of RAM. 





Update:

Found some useful links on how to implement custom distance metrics for knn: 

https://towardsdatascience.com/machine-learning-basics-with-the-k-nearest-neighbors-algorithm-6a6e71d01761

https://stackoverflow.com/questions/32848218/how-to-define-a-custom-similarity-measure




Ideas for time thresholds: if more than an hour apart, we cannot consider these to be in the same time frame


Ideas for metric:
- Weighted Euclidean Distance (with a greater emphasis on time similarity)
2022-03-07 check in: alp

Glad to hear about the new discovery. Would strongly recommend spending some time soon to catch up. A good place to start would be to replicate the results from the paper and see where you want to go from there.
