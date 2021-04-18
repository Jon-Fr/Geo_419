
import tkinter
import urllib.request
from tkinter import filedialog
import os.path
import zipfile
import rasterio
import numpy

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from rasterio.plot import show

def browseFiles(): # öffnet Ordnerauswahl
	filename = filedialog.askdirectory()
	return filename
    
def downloadZip(): # downloadZip
    if not os.path.exists("Data.zip"):
        url = "https://upload.uni-jena.de/data/605dfe08b61aa9.92877595/GEO419_Testdatensatz.zip"
        urllib.request.urlretrieve(url, "Data.zip")

def extractZip(): # Zip extrahieren
    if not os.path.exists("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC.tif"):
        data = zipfile.ZipFile("Data.zip", "r")
        data.extractall()

def calculateLog(): # logarithmisch skalieren
    if not os.path.exists("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC_log.tif"):
        dataset = rasterio.open("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC.tif")
        data_array = dataset.read(1)
        data_array_log = 10*numpy.log10(data_array, out=numpy.zeros_like(data_array), where=(data_array != 0))
        new_dataset = rasterio.open("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC_log.tif", "w", driver="GTiff",
                                    height=data_array_log.shape[0], width=data_array_log.shape[1], count=1,
                                    dtype=data_array_log.dtype, crs="EPSG:32632", transform=dataset.transform)
        new_dataset.write(data_array_log, 1)
        new_dataset.close()


def remoteSensing419(fileF = ''):
    print(fileF)
    window = Tk()
    # erstellt das Hauptfenster
    # Hauptfenster konfiguration
    window.configure(bg = 'white')
    window.wm_attributes('-topmost', 1)
    window.withdraw() # versteckt Hauptfenster vorerst
    fileSet = 0 # 1: Pfad erfolgreich gesetzt 0: Pfad nicht gesetzt
    if os.path.isdir(fileF):
        os.chdir(fileF)
        fileSet = 1 # Pfad existiert und wurde gesetzt
    else: 
        try: # Pfad existiert nicht und es wird versucht, ihn zu erstellen
            os.makedirs(fileF)
            fileSet = 1
        except: # Pfad konnte nicht erstellt werden, Pfad muss manuell ausgewählt werden
            fileF = browseFiles()
            try:
                os.chdir(fileF)
                fileSet = 1
            except: # Falls kein Pfad ausgewählt wurde (z.B. wenn FileDialog geschlossen wird)
                error = Label(window, text = "Abreitsverzeichnis konnte nicht gesetzt werden")
                error.pack()
                window.deiconify()
    if fileSet == 1: # Nur wenn Pfad gesetzt wurde
        downloadZip()
        extractZip()
        calculateLog()
        window.deiconify()
        
        # Erstellen des Ergebnis-Plots mit allen möglichen Einstellungen
        
        resultData = rasterio.open("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC_log.tif")
        fig = Figure(figsize=(5, 4), dpi=100)

        canvas1 = FigureCanvasTkAgg(fig, master=window)
        canvas1.draw()
        toolbar = NavigationToolbar2Tk(canvas1,window)
        toolbar.update()
        toolbar.pack(side=tkinter.TOP, fill=tkinter.X, padx=8)
        canvas1.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1, padx=10, pady=5)
        canvas1._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1, padx=10, pady=5)
        ax = fig.add_subplot(111)
        fig.subplots_adjust(bottom=0, right=1, top=1, left=0, wspace=0, hspace=0)
        
        resultData = rasterio.open("S1B__IW___A_20180828T171447_VV_NR_Orb_Cal_ML_TF_TC_log.tif")
        show(resultData, ax=ax, cmap='gist_gray')
        plt.close()
        ax.set(title="",xticks=[], yticks=[])
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        canvas1.draw()
        
        
        
    window.mainloop()
    # Hauptschleife (wird hier nur einmal durchlaufen)
    # Funktion wird dadurch erst beendet, wenn Programm beendet wird (Teil der Aufgabenstellung)

if __name__ == '__main__':
    remoteSensing419()