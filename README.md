# GEO_419
Dieses Programm wurde dazu entwickelt um einzelne Sentinel-1 Szenen zu downloaden, logarithmische zu skalieren und zu visualisieren. Das Hauptskript dieses Programms enthält zu diesem Zweck Funktionen, die das Downloaden und Entpacken von ZIP-Dateien sowie das logarithmische skalieren und visualisieren von GeoTIFFs umfassen. Die Visualisierung in der Hauptfunktion ist speziell auf Radar Rückstreuintensität in gamma nought (γ0) zugeschnitten. Die übrigen Funktionen können auch für andere Daten verwendet werden.

## Installation
Im Folgenden Abschnitt wird die Installation des Programms für Microsoft Windows und Ubuntu beschrieben. 

#### Microsoft Windows
Klonen Sie zunächst dieses Repository auf Ihr lokales System. 

Wenn Sie [Anaconda][1] benutzen können Sie das Programm anschließend installieren, indem Sie die beiden folgenden Befehle in ein Python Terminal eingeben.
```sh
conda install -c conda-forge rasterio
pip install "Pfad zum Programm" --use-feature=in-tree-build
```

Alternativ lässt sich das Programm auch über die Eingabe folgender Befehle in ein Python Terminal installieren.
```sh
pip install pipwin
pipwin install gdal
pipwin install rasterio
pip install "Pfad zum Programm" --use-feature=in-tree-build
```

#### Ubuntu 
Klonen Sie zunächst dieses Repository auf Ihr lokales System. 

Installieren Sie Tkinter (wenn nicht bereits vorhanden).
```sh
sudo apt-get install python3-tk
```

Anschließend können Sie das Programm installieren, indem Sie folgenden Befehl in ein Python Terminal eingeben.
```sh
pip install "Pfad zum Programm" --use-feature=in-tree-build
```

## Dokumentation 
Die Dokumentation der Funktionen ist [hier][2] zu finden.

[1]: https://www.anaconda.com/
[2]: https://jon-fr.github.io/Geo_419_Dokumentation/Geo_419.html
