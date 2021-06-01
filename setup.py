import os
import sys
from setuptools import setup, find_packages

directory = os.path.abspath(os.path.dirname(__file__))
if sys.version_info >= (3, 0):
    with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
else:
    with open(os.path.join(directory, 'README.md')) as f:
        long_description = f.read()

os.chdir("C:/Users/frank/Desktop/Test/Geo_419-master")

if not os.path.exists("requirements.txt"):
    print("Bitte stellen Sie sicher, dass sich die Datei requirements.txt in ihrem working directory befindet.")
    sys.exit()
else:
    with open("requirements.txt", "r") as req:
        requires = []
        for line in req:
            requires.append(line.strip())
try:
    setup(name="Geo_419",
          packages=find_packages(),
          include_package_data=True,
          description="A program for logarithmic scaling and visualizing of Sentinel-1 scenes.",
          version="1.2.0",
          keywords="SAR, Histogram Equalization",
          python_requires="==3.7",
          setup_requires=["numpy"],
          install_requires=requires,
          classifiers=[
              "Programming Language :: Python"
              "Operating System :: Microsoft :: Windows",
              "Topic :: Scientific/Engineering :: Visualization",
              "Intended Audience :: Science/Research",
          ],
          url="https://github.com/Jon-Fr/Geo_419",
          author="Jonathan Frank",  # Fabian Schreiter, Jonathan Frank; we do not know how to add a second author
          author_email="jonathan.frank@uni-jena.de",
          license="GPL-3",
          zip_safe=False,
          long_description=long_description,
          long_description_content_type="text/markdown")
except SystemExit:
    print("\nFehler bei ausführen des setup. Der Fehler wurde wahrscheinlich darduch Verursacht, dass rastio nicht"
          " installiert werden konnte.\nBitte führen Sie die installation von rasterio manuell durch (mehr Informationen "
          "dazu in der README) und versuchen es anschließend erneut.")

