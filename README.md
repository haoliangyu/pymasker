# pymasker

Pymasker is a python package to generate various masks from the Landsat 8 Quality Assessment band and MODIS land products.

## Installation

The package can be shipped to your computer using pip.

	pip install pymasker

Or just install it with the source code.

	python setup.py install

This package depends on [**numpy**](http://www.numpy.org/) and [**GDAL**](https://pypi.python.org/pypi/GDAL/).

An ArcMap python toolbox based on this package could be find [**here**](https://github.com/dz316424/arcmasker).

## Use Example

### Python

For Landsat 8 Quality Accessment band

``` python
from pymasker import LandsatMasker
from pymasker import LandsatConfidence

# load the QA band directly
masker = LandsatMasker('LC80170302014272LGN00_BQA.TIF')

# algorithm has high confidence that this condition exists (67-100 percent confidence)
conf = LandsatConfidence.high

# Get mask indicating cloud pixels with high confidence
mask = masker.get_cloud_mask(conf)

# save the result
masker.save_tif(mask, 'result.tif')
```

For MODIS land products

``` python
from pymasker import ModisMasker
from pymasker import ModisQuality

# load the QA band directly
masker = ModisMasker('MOD09GQ.A2015025.h12v04.005.2015027064556.hdf')

# Corrected product produced at ideal quality for all bands.
quality = ModisQuality.high

# Create a MODIS QA masker
mask = masker.get_qa_mask(conf)

# save the result
masker.save_tif(mask, 'result.tif')
```

### Command Line

``` bash
pymasker -s landsat -i landsat.tif -o mask.tif -c high -t cirrus
```

General parameters:

```
-s, --source SOURCE
                      source type: landsat, modis
-i, --input INPUT
                      input image file path
-o, --output OUTPUT
                      output raster path
```

Landsat parameters:

```
-c, --confidence CONFIDENCE
                      level of confidence that a condition exists in a landsat image: high, medium, low, undefined, none
-t, --target TARGET
                      target object: cloud, cirrus, water, vegetation, snow
```

MODIS parameters:

```
-q, --quality QUALITY
                      Level of data quality of MODIS land products at each pixel: high, medium, low, low_cloud
```

## More Detail

The following two articles explains the mechanism behind the tool in detail.

* [Landsat 8 Quality Assessment band](http://haoliangyu.github.io/2015/01/18/Making-masks-with-Landsat-8-Quality-Assessment-band-using-Python/)

* [MODIS land products](http://haoliangyu.github.io/2015/02/19/Making-masks-from-Quality-Control-bits-of-MODIS-land-products-in-Python-Update/)

## For JavaScript Developer

[node-qa-masker](https://github.com/haoliangyu/node-qa-masker) provides the same masking functionality in NodeJS.

## Change Log

* **0.3.1**
  * Simplify the initialization of ModisMasker

* **0.3.0**
  * **BREAKING CHANGE** change most class and function names according to pep8
  * add command line tool
