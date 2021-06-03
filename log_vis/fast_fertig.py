import tkinter as tk
import urllib.request
from tkinter import filedialog, Tk
import os.path
import zipfile
import rasterio
import numpy as np

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from rasterio.plot import show


def browseFiles():  # öffnet Ordnerauswahl
    filename = filedialog.askdirectory()
    return filename


def downloadZip():  # downloadZip
    if not os.path.exists("Data.zip"):
        url = "https://upload.uni-jena.de/data/605dfe08b61aa9.92877595/GEO419_Testdatensatz.zip"
        urllib.request.urlretrieve(url, "Data.zip")


def extractZip():  # Zip extrahieren
    if not os.path.exists("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC.tif"):
        data = zipfile.ZipFile("Data.zip", "r")
        data.extractall()


def calculateLog():  # logarithmisch skalieren
    if not os.path.exists("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC_log.tif"):
        dataset = rasterio.open("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC.tif")
        data_array = dataset.read(1)
        nodata_value = dataset.nodatavals
        nodata_value = nodata_value[0]
        nodata_mask = data_array == nodata_value
        data_array[nodata_mask] = np.nan
        data_array_log = 10 * np.log10(data_array, out=np.zeros_like(data_array), where=(data_array != 0))
        new_dataset = rasterio.open("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC_log.tif", "w", driver="GTiff",
                                    height=data_array_log.shape[0], width=data_array_log.shape[1], count=1,
                                    dtype=data_array_log.dtype, crs="EPSG:32632", transform=dataset.transform,
                                    nodata=np.nan)
        new_dataset.write(data_array_log, 1)
        new_dataset.close()


def histogramEqualization():
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
    dal_dict = {}  # the utilization of a dictionary greatly increase the performance
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


def remoteSensing419(fileF=''):
    print(fileF)
    window: Tk = tk.Tk()
    # erstellt das Hauptfenster
    # Hauptfenster konfiguration
    window.configure(bg='white')
    window.wm_attributes('-topmost', 1)  # Neues Fenster (FileDialog) erscheint über allen anderen
    window.withdraw()  # versteckt Hauptfenster vorerst
    fileSet = 0  # 1: Pfad erfolgreich gesetzt 0: Pfad nicht gesetzt
    if os.path.isdir(fileF):
        os.chdir(fileF)
        fileSet = 1  # Pfad existiert und wurde gesetzt
    else:
        try:  # Pfad existiert nicht und es wird versucht, ihn zu erstellen
            os.makedirs(fileF)
            fileSet = 1
        except:  # Pfad konnte nicht erstellt werden, Pfad muss manuell ausgewählt werden
            fileF = browseFiles()
            try:
                os.chdir(fileF)
                fileSet = 1
            except:  # Falls kein Pfad ausgewählt wurde (z.B. wenn FileDialog geschlossen wird)
                error = tk.Label(window, text="Abreitsverzeichnis konnte nicht gesetzt werden")
                error.pack()
                window.title("Fehler")
                window.deiconify()
    if fileSet == 1:  # Nur wenn Pfad gesetzt wurde
        try:
            downloadZip()
        except:
            error = tk.Label(window, text="Daten konnten nicht heruntergeladen werden")
            error.pack()
            window.title("Fehler")
            window.deiconify()
        else:
            extractZip()
            calculateLog()
            if not os.path.exists("Only_for_visualisation.tif"):
                explanationText = """Zur besseren Visualiserung wird eine Histogramm-Angleichung empfohlen. Je nach Rechenleistung kann dies jedoch etwas Zet in Anspruch nehmen.\n\nMöchten Sie die Histogramm-Angleichung durchführen?"""
                decisionBox = tk.messagebox.askquestion('Histogramm-Angleichung', explanationText)
                if decisionBox == 'yes':
                    histogramEqualization()

            window.deiconify()
            window.wm_attributes('-topmost', 0)  # Einstellung zurücksetzen auf 0
            # Schieberegler erscheint ansonsten unter dem Bild versteckt

            window.title("Rasterdatei")
            # Erstellen des Ergebnis-Plots mit allen möglichen Einstellungen
            # window.geometry("1000x1000")

            if os.path.exists("Only_for_visualisation.tif"):
                explanationText = """Soll das Ergebnis der Histogramm-Angleichung angezigt werden?\nWenn Sie nein wählen wird das Ergebnis der logarithmischen Skalierung angezeigt."""
                decisionBox = tk.messagebox.askquestion("Anzeige", explanationText)

                if decisionBox == "yes":
                    resultData = rasterio.open("Only_for_visualisation.tif")
                    resultDataArray = resultData.read(1)
                    fig, ax = plt.subplots(figsize=(7.445, 5.4475), dpi=100)
                    plt.rc('font', size=10)  # Festlegung der Schriftgröße der Legende
                    plt.imshow(resultDataArray, cmap="plasma")
                    cbar = plt.colorbar(orientation="vertical", ticks=[0, 255])
                    cbar.ax.set_yticklabels(["niedrig", "hoch"])
                    cbar.set_label("Rückstreuungsintensität", labelpad=-30)
                    plt.rc('font', size=12)  # Festlegung der Schriftgröße der Achsen und des Titels
                    plt.title("", fontsize=12, fontweight="bold")
                    plt.xlabel("Rechtswert [m]", labelpad=10)
                    plt.ylabel("Hochwert [m]", labelpad=10)

                    canvas1 = FigureCanvasTkAgg(fig, master=window)
                    canvas1.draw()
                    toolbar = NavigationToolbar2Tk(canvas1, window)
                    toolbar.update()
                    toolbar.pack(side=tk.TOP, fill=tk.X, padx=8)
                    canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=10, pady=5)
                    canvas1._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=10, pady=5)
                    fig.subplots_adjust(bottom=0.07, right=1, top=0.97, left=0.15, wspace=0, hspace=0)
                    show(resultData, ax=ax, cmap='plasma')

                    ax.spines["top"].set_visible(True)
                    ax.spines["right"].set_visible(True)
                    ax.spines["left"].set_visible(True)
                    ax.spines["bottom"].set_visible(True)
                    canvas1.draw()

                    plt.close()
                    resultData.close()

                if decisionBox == "no":
                    resultData = rasterio.open("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC_log.tif")
                    resultDataArray = resultData.read(1)
                    fig, ax = plt.subplots(figsize=(7.445, 5.4475), dpi=100)
                    plt.rc('font', size=10)  # Festlegung der Schriftgröße der Legende
                    plt.imshow(resultDataArray, cmap="Greys_r")
                    cbar = plt.colorbar(orientation="vertical")
                    cbar.set_label("Rückstreuungsintensität [10 * log$_{10}(\gamma)$]", labelpad=9)
                    plt.rc('font', size=12)  # Festlegung der Schriftgröße der Achsen und des Titels
                    plt.title("", fontsize=12, fontweight="bold")
                    plt.xlabel("Rechtswert [m]", labelpad=10)
                    plt.ylabel("Hochwert [m]", labelpad=10)

                    canvas1 = FigureCanvasTkAgg(fig, master=window)
                    canvas1.draw()
                    toolbar = NavigationToolbar2Tk(canvas1, window)
                    toolbar.update()
                    toolbar.pack(side=tk.TOP, fill=tk.X, padx=8)
                    canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=10, pady=5)
                    canvas1._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=10, pady=5)
                    fig.subplots_adjust(bottom=0.07, right=0.97, top=0.97, left=0.15, wspace=0, hspace=0)
                    show(resultData, ax=ax, cmap="Greys_r")

                    ax.spines["top"].set_visible(True)
                    ax.spines["right"].set_visible(True)
                    ax.spines["left"].set_visible(True)
                    ax.spines["bottom"].set_visible(True)
                    canvas1.draw()

                    plt.close()
                    resultData.close()

            else:
                resultData = rasterio.open("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC_log.tif")
                resultDataArray = resultData.read(1)
                fig, ax = plt.subplots(figsize=(7.445, 5.4475), dpi=100)
                plt.rc('font', size=10)  # Festlegung der Schriftgröße der Legende
                plt.imshow(resultDataArray, cmap="Greys_r")
                cbar = plt.colorbar(orientation="vertical")
                cbar.set_label("Rückstreuungsintensität [10 * log$_{10}(\gamma)$]", labelpad=9)
                plt.rc('font', size=12)  # Festlegung der Schriftgröße der Achsen und des Titels
                plt.title("", fontsize=12, fontweight="bold")
                plt.xlabel("Rechtswert [m]", labelpad=10)
                plt.ylabel("Hochwert [m]", labelpad=10)

                canvas1 = FigureCanvasTkAgg(fig, master=window)
                canvas1.draw()
                toolbar = NavigationToolbar2Tk(canvas1, window)
                toolbar.update()
                toolbar.pack(side=tk.TOP, fill=tk.X, padx=8)
                canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=10, pady=5)
                canvas1._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=10, pady=5)
                fig.subplots_adjust(bottom=0.07, right=0.97, top=0.97, left=0.15, wspace=0, hspace=0)
                show(resultData, ax=ax, cmap="Greys_r")

                ax.spines["top"].set_visible(True)
                ax.spines["right"].set_visible(True)
                ax.spines["left"].set_visible(True)
                ax.spines["bottom"].set_visible(True)
                canvas1.draw()

                plt.close()
                resultData.close()

    # File schließen
    window.mainloop()

    # Hauptschleife (wird hier nur einmal durchlaufen)
    # Funktion wird dadurch erst beendet, wenn Programm beendet wird (Teil der Aufgabenstellung)


if __name__ == '__main__':
    remoteSensing419()