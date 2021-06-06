import tkinter as tk
import urllib.request
from tkinter import filedialog, Tk
import os.path
import zipfile
import rasterio
import numpy as np

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
from rasterio.plot import show


def browseFiles():
    """
    Öffnet die Verzeichnisauswahl, damit das Arbeits/Ausgabeverzeichnis festgelegt werden kann.

    Parameters
    ----------

    Returns
    -------

    """
    filename = filedialog.askdirectory()
    return filename


def downloadZip(url="https://upload.uni-jena.de/data/605dfe08b61aa9.92877595/GEO419_Testdatensatz.zip"):
    """
    Downloadet eine zip-Datei von der angegebenen URL, legt sie im Arbeits/Ausgabeverzeichnis ab und gibt den Namen
    der zip-Datei zurück.
    Der download wird nur ausgeführt, wenn im Arbeits/Ausgabeverzeichnis noch keine zip-Datei mit dem gleichen Namen
    existiert.

    Parameters
    ----------
    url: str
        die URL einer zip-Datei.

    Returns
    -------
    str
        der Name der zip-Datei (inklusive Dateiendung)
    """
    name = url[url.rindex("/")+1:len(url)]
    if not os.path.exists(name):
        urllib.request.urlretrieve(url, name)
    return name

def extractZip(zip="GEO419_Testdatensatz.zip"):
    """
    Entpackt die angegebenen zip-Datei ins Arbeits/Ausgabeverzeichnis und gibt den Namen der entpackten Datei
    zurück, insofern es denn nur eine Datei ist.
    Die zip-Datei wird allerdings nur entpackt, wenn sich im Arbeits/Ausgabeverzeichnis keine Datei befindet, die den
    gleichen Namen hat wie eine Datei innerhalb der zip Datei.

    Parameters
    ----------
    zip: str
        Pfad zu einer zip-Datei bzw. der Name der zip-Datei inkluisve .zip, wenn sich die Datei im
        Arbeits/Ausgabeverzeichnis befindet.

    Returns
    -------
    str
        der Name der entpackten Datei (inklusive Dateiendung)
    """
    temp = zipfile.ZipFile(zip, "r")
    content = zipfile.ZipFile.namelist(temp)
    zipfile.ZipFile.close(temp)
    index = 0
    while index < len(content):
        if not os.path.exists(content[index]):
            extract = "yes"
        else:
            extract = "no"
            break
        index = index + 1
    if extract == "yes":
        data = zipfile.ZipFile(zip, "r")
        data.extractall()
        zipfile.ZipFile.close(data)
    if len(content) == 1:
        name = content[0]
        return name

def calculateLog(tif="S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC.tif"):
    """
    Skaliert die Werte einer TIF-Datei logarithmisch, exportiert das Ergebnis (als TIF-Datei) ins
    Arbeits/Ausgabeverzeichnis und gibt den Namen der Ergebnisdatei zurück.
    Die Funktion überprüft allerdings als erstes, ob sich im Arbeits/Ausgabeverzeichnis eine Datei mit dem gleichen
    Namen wie die potentielle Ergebnisdatei befindet. Sollte dies der Fall sein, gibt die Funktion nur den Namen der
    Datei zurück.

    Parameters
    ----------
    tif: str
        Pfad zu einer TIF-Datei bzw. der Name der TIF-Datei inkluisve .tif, wenn sich die Datei im
        Arbeits/Ausgabeverzeichnis befindet.

    Returns
    -------
    str
        der Name der Ergebnisdatei (inklusive Dateiendung)
    """
    temp = tif[0:tif.rindex(".")]
    name = "{}_log.tif".format(temp)
    if not os.path.exists(name):
        dataset = rasterio.open(tif)
        data_array = dataset.read(1)
        nodata_value = dataset.nodatavals
        nodata_value = nodata_value[0]
        nodata_mask = data_array == nodata_value
        data_array[nodata_mask] = np.nan
        data_array_log = 10 * np.log10(data_array, out=np.zeros_like(data_array), where=(data_array != 0))
        new_dataset = rasterio.open(name, "w", driver="GTiff",
                                    height=data_array_log.shape[0], width=data_array_log.shape[1], count=1,
                                    dtype=data_array_log.dtype, crs="EPSG:32632", transform=dataset.transform,
                                    nodata=np.nan)
        new_dataset.write(data_array_log, 1)
        new_dataset.close()
    return name


def histogramEqualization(tif="S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC_log.tif"):
    """
    Führt eine Histogramm-Angleichung durch, exportiert das Ergebnis (als TIF-Datei) in den Arbeits/Ausgabeverzeichnis
    und gibt den Namen der Ergebnisdatei zurück.
    Die Funktion überprüft allerdings als erstes, ob sich im Arbeits/Ausgabeverzeichnis eine Datei mit dem gleichen
    Namen wie die potentielle Ergebnisdatei befindet. Sollte dies der Fall sein, gibt die Funktion nur den Namen der
    Datei zurück.

    Parameters
    ----------
    tif: str
        Pfad zu einer TIF-Datei bzw. der Name der TIF-Datei inkluisve .tif, wenn sich die Datei im
        Arbeits/Ausgabeverzeichnis befindet.

    Returns
    -------
    str
        der Name der Ergebnisdatei (inklusive Dateiendung)
    """
    temp = tif[0:tif.rindex(".")]
    name = "{}_Hist_ang.tif".format(temp)
    if not os.path.exists(name):
        explanationText = "Zur besseren Visualiserung wird eine Histogramm-Angleichung empfohlen. Je nach Rechenleistung und Dateigröße kann dies jedoch etwas Zet in Anspruch nehmen.\n\nMöchten Sie die Histogramm-Angleichung durchführen?"
        decisionBox = tk.messagebox.askquestion('Histogramm-Angleichung', explanationText)
        if decisionBox == 'yes':
            # open GeoTiff
            dataset_log = rasterio.open(tif)
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
            vis_dataset = rasterio.open(name, "w", driver="GTiff",
                                        height=dal_eq.shape[0], width=dal_eq.shape[1], count=1,
                                        dtype=dal_eq.dtype, crs="EPSG:32632", transform=dataset_log.transform,
                                        nodata=np.nan)
            vis_dataset.write(dal_eq, 1)
            vis_dataset.close()
    return name


def remoteSensing419(fileF=''):
    """
    Die Hauptfunktion des Programms, innerhalb der die vorher definierten Funktionen aufgerufen werden. Am Ende der 
    Funktion findet die Visualisierung des Ergebnis statt.

    Parameters
    ----------
    fileF: str
        Pfad zum Arbeits/Ausgabeverzeichnis

    Returns
    -------
    """
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
                error = tk.Label(window, text="Arbeitsverzeichnis konnte nicht gesetzt werden")
                error.pack()
                window.title("Fehler")
                window.deiconify()
    if fileSet == 1:  # Nur wenn Pfad gesetzt wurde
        try:
            zip_name=downloadZip()
        except:
            error = tk.Label(window, text="Daten konnten nicht heruntergeladen werden")
            error.pack()
            window.title("Fehler")
            window.deiconify()
        else:
            tif_name=extractZip(zip_name)
            tif_log_name=calculateLog(tif_name)
            tif_hist_eq=histogramEqualization(tif_log_name)

            window.deiconify()
            window.wm_attributes('-topmost', 0)  # Einstellung zurücksetzen auf 0
            # Schieberegler erscheint ansonsten unter dem Bild versteckt

            window.title("Rasterdatei")
            # Erstellen des Ergebnis-Plots mit allen möglichen Einstellungen
            # window.geometry("1000x1000")

            plot_log = "yes"
            if os.path.exists(tif_hist_eq):
                explanationText = "Soll das Ergebnis der Histogramm-Angleichung angezigt werden?\nWenn Sie nein wählen wird das Ergebnis der logarithmischen Skalierung angezeigt."
                decisionBox = tk.messagebox.askquestion("Anzeige", explanationText)

                if decisionBox == "yes":
                    plot_log = "no"
                    resultData = rasterio.open(tif_hist_eq)
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

            if plot_log == "yes":
                resultData = rasterio.open(tif_log_name)
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

    
if __name__ == '__main__':
    remoteSensing419()
