# import packages
import os
import os.path
import urllib.request
import zipfile
import rasterio
import numpy as np
from matplotlib import pyplot as plt
from rasterio.plot import show

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
    # create a new GeoTIFF with the log scaled data
    new_dataset = rasterio.open("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC_log.tif", "w", driver="GTiff",
                                height=data_array_log.shape[0], width=data_array_log.shape[1], count=1,
                                dtype=data_array_log.dtype, crs="EPSG:32632", transform=dataset.transform,
                                nodata=np.nan)
    new_dataset.write(data_array_log, 1)
    new_dataset.close()

# perform histogram equalization (if necessary)
if not os.path.isfile("Only_for_visualisation.tif"):
    # open GeoTiff
    dataset_log = rasterio.open("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC_log.tif")
    # covert data to np array
    dal = dataset_log.read(1)
    # flatt the array
    dal_flatt = dal.flatten()
    # make sure that all pixel values are >= 0 or the normalization will get messed up
    dal_min = np.nanmin(dal_flatt)
    if dal_min < 0:
        dal_flatt = dal_flatt - dal_min
    # frequency count of each pixel
    not_nan_dal = dal_flatt >= dal_min
    fre = (np.unique(dal_flatt[not_nan_dal], return_counts=True))
    dal_sum = fre[1] * fre[0]
    # cumulative sum
    c_sum = np.cumsum(dal_sum)
    # normalization of the pixel values
    c_sum_min = c_sum.min()
    c_sum_max = c_sum.max()
    norm = (c_sum - c_sum_min) * 255
    n = c_sum_max - c_sum_min
    uniform_norm = norm / n
    # create array with the new pixel values at the right position
    dal_eq = np.zeros(dal_flatt.shape[0])
    dal_list = fre[0].tolist()
    dal_dict = {}   # the utilization of a dictionary greatly increase the performance
    for i in range(0, len(dal_list)):
        dal_dict[dal_list[i]] = uniform_norm[i]
    for i in range(dal_flatt.shape[0]):
        if dal_flatt[i] >= dal_min:
            dal_eq[i] = dal_dict[dal_flatt[i]]
        else:
            dal_eq[i] = np.nan
    # reshaping the flattened matrix to its original shape
    dal_eq = np.reshape(a=dal_eq, newshape=dal.shape)
    # create a new GeoTIFF for visualisation
    vis_dataset = rasterio.open("Only_for_visualisation.tif", "w", driver="GTiff",
                                height=dal_eq.shape[0], width=dal_eq.shape[1], count=1,
                                dtype=dal_eq.dtype, crs="EPSG:32632", transform=dataset_log.transform,
                                nodata=np.nan)
    vis_dataset.write(dal_eq, 1)
    vis_dataset.close()

# Visualization of the results
# open GeoTiff
dataset_eq = rasterio.open("Only_for_visualisation.tif")
# covert data to np array
dal_eq = dataset_eq.read(1)
# plotting the image
fig, ax = plt.subplots(figsize=(14.89, 10.895)) # Festlegung der Größe des Plots
plt.rc('font', size=16) # Festlegung der Schriftgröße der Legende
# Legende erstellen
plt.imshow(dal_eq, cmap="plasma")
cbar = plt.colorbar(orientation="vertical", ticks=[0, 255])
cbar.ax.set_yticklabels(["niedrig", "hoch"])
cbar.set_label("Rückstreuungsintensität", labelpad=-30)
show((dataset_eq, 1), transform=dataset_eq.transform, ax=ax, cmap="plasma") # Verwendung von rasterio.show um die Korrdinatenwerte als Achsen zu erhalten
plt.rc('font', size=16) # Festlegung der Schriftgröße der Achsen und des Titels
plt.title("", fontsize=12, fontweight="bold")
plt.xlabel("Rechtswert [m]", labelpad=10)
plt.ylabel("Hochwert [m]", labelpad=10)
plt.show() # Dürchführen des eigentlichen Plottens



