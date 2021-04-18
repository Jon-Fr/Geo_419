# import packages
import os
import os.path
import urllib.request
import zipfile
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from rasterio.plot import show as raster_show

# set working directory
os.chdir("C:/Users/frank/Desktop/Uni/Master/Semester_1/Geo_419/Abschlussaufgabe_Daten_usw")

# download data (if necessary)
if not os.path.isfile("Data.zip"):
    url = "https://upload.uni-jena.de/data/605dfe08b61aa9.92877595/GEO419_Testdatensatz.zip"
    urllib.request.urlretrieve(url, "Data.zip")

# unzip data (if necessary)
if not os.path.isfile("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC.tif"):
    data = zipfile.ZipFile("Data.zip", "r")
    data.extractall()

# read data and compute result (if necessary)
# open GeoTiff
if not os.path.isfile("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC_log.tif"):
    dataset = rasterio.open("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC.tif")
    # covert data to numpy array
    data_array = dataset.read(1)
    # get nodata value
    nodata_value = dataset.nodatavals
    nodata_value = nodata_value[0]
    # set nodata pixels to np.nan
    nodata_mask = data_array == nodata_value
    data_array[nodata_mask] = np.nan
    # change scaling to log
    data_array_log = 10 * np.log10(data_array, out=np.zeros_like(data_array), where=(data_array != 0))
    # create a new file with the log scaled data
    new_dataset = rasterio.open("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC_log.tif", "w", driver="GTiff",
                                height=data_array_log.shape[0], width=data_array_log.shape[1], count=1,
                                dtype=data_array_log.dtype, crs="EPSG:32632", transform=dataset.transform,
                                nodata=np.nan)
    new_dataset.write(data_array_log, 1)
    new_dataset.close()

# display result
# open GeoTiff
dataset_log = rasterio.open("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC_log.tif")
# covert data to np array
data_array_log = dataset_log.read(1)

"""
# perform contrast stretching
stretched_data_array_log = np.zeros((data_array_log.shape[0], data_array_log.shape[1]), dtype=data_array_log.dtype)
minimum_value = np.nanmin(data_array_log)
maximum_value = np.nanmax(data_array_log)
for y in range(data_array_log.shape[0]):
    for x in range(data_array_log.shape[1]):
        if data_array_log[y, x] >= minimum_value:
            stretched_data_array_log[y, x] = 255 * (data_array_log[y, x] - minimum_value) / \
                                             (maximum_value - minimum_value)
        else:
            stretched_data_array_log[y, x] = np.nan

plt.hist(data_array_log.flatten())
plt.show()
plt.hist(stretched_data_array_log.flatten())
plt.show()
"""

fig, ax = plt.subplots(figsize=(14.89, 10.895))
plt.imshow(data_array_log)
raster_show(dataset_log, ax=ax)
plt.title("", fontsize=12, fontweight="bold")
plt.xlabel("Rechtswert in")
plt.ylabel("Hochwert in")
plt.colorbar()
plt.show()


