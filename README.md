# GEO_419
Dieses Pakete wurde dazu entwicklet um einzelne Sentinel-1 Szenen zu downloaden, logarithmische zu skalieren und zu visualisieren. Das Hauptskript dieses Paketes enthält zu diesem Zweck Funktionen, die das Downloaden und entpacken von ZIP-Dateien sowie das logarithmische skalieren und visualisieren von GeoTIFFs umfassen. Die Visualisierung in der Hauptfunktion ist speziell auf Radar Rückstreuintensität in gamma nought (γ0) zugeschnitten. Die übrigen Funktionen können auch für andere Daten verwendet werden.

## Installation
Im Folgenden Abschnitt wird die Installation des Paketes für Microsoft Windows beschrieben.

```sh
conda install -c conda-forge rasterio
pip install "Pfad zum Paket" --use-feature=in-tree-build
```

```sh
pip install pipwin
pipwin install gdal
pipwin install rasterio
pip install "Pfad zum Paket" --use-feature=in-tree-build
```
