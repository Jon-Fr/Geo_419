# import packages
import os
import urllib.request
import zipfile
import rasterio
import numpy
import matplotlib.pyplot
from rasterio.plot import show as raster_show


# set working directory
os.chdir("C:/Users/frank/Desktop/Uni/Master/Semester_1/Geo_419/Abschlussaufgabe")

# download data
url = "https://upload.uni-jena.de/data/605dfe08b61aa9.92877595/GEO419_Testdatensatz.zip"
urllib.request.urlretrieve(url, "Data.zip")

# unzip data
data = zipfile.ZipFile("Data.zip", "r")
data.extractall()

# read data
dataset = rasterio.open("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC.tif")

# covert data to numpy array
data_array = dataset.read(1)

# change scaling to log
data_array_log = 10*numpy.log10(data_array, out=numpy.zeros_like(data_array), where=(data_array != 0))

# create a new file with the log scaled data
new_dataset = rasterio.open("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC_log.tif", "w", driver="GTiff",
                            height=data_array_log.shape[0], width=data_array_log.shape[1], count=1,
                            dtype=data_array_log.dtype, crs="EPSG:32632", transform=dataset.transform)
new_dataset.write(data_array_log, 1)
new_dataset.close()

# display result
dataset_log = rasterio.open("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC_log.tif")
raster_show(dataset_log)


