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

if not os.path.exists("requirements.txt"):
    print("Bitte stellen Sie sicher, dass sich die Datei requirements.txt in ihrem working directory befindet.")
    sys.exit()
else:
    with open("requirements.txt", "r") as req:
        requires = []
        for line in req:
            requires.append(line.strip())
            

setup(name="Geo_419",
    packages=find_packages(),
    include_package_data=True,
    description="Ein Programm zum logarithmischen skalieren und visualisieren von Sentinel-1 Szenen.",
    version="1.0.0",
    keywords="SAR, Histogram-Angleichung",
    python_requires=">=3.7.0",
    setup_requires=["numpy"],
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Visualization",
        "Intended Audience :: Science/Research",
    ],
    url="https://github.com/Jon-Fr/Geo_419",
    author="Jonathan Frank",  # Fabian Schreiter und Jonathan Frank; Ist es möglich einen zweiten Autor hinzuzufügen?
    author_email="jonathan.frank@uni-jena.de",
    license="GPL-3",
    zip_safe=False,
    long_description=long_description,
    long_description_content_type="text/markdown")


