# GEO_419
Dieses Pakete wurde dazu entwicklet um einzelne Sentinel-1 Szenen zu downloaden, logarithmische zu skalieren und zu visualisieren. Das Hauptskript dieses Paketes enthält zu diesem Zweck Funktionen, die das Downloaden und entpacken von ZIP-Dateien sowie das logarithmische skalieren und visualisieren von GeoTIFFs umfassen. Die Visualisierung in der Hauptfunktion ist speziell auf Radar Rückstreuintensität in gamma nought (γ0) zugeschnitten. Die übrigen Funktionen können auch für andere Daten verwendet werden.

## Installation
Im Folgenden Abschnitt wird die Installation des Paketes für Microsoft Windows beschrieben. 

Klonen Sie zunächst dieses Repository auf Ihr lokales System. 

Wenn Sie [Anaconda][1] benutzen können Sie das Paket anschließend installieren, indem Sie die beiden folgenden befehle in ein Python Terminal eingeben.
```sh
conda install -c conda-forge rasterio
pip install "Pfad zum Paket" --use-feature=in-tree-build
```

Alternativ lässt sich das Pakete auch über die Eingabe folgender befehle in eine Python Terminal installieren.
```sh
pip install pipwin
pipwin install gdal
pipwin install rasterio
pip install "Pfad zum Paket" --use-feature=in-tree-build
```

[1]: https://www.anaconda.com/
