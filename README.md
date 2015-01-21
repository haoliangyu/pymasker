# pymasker

Pymasker is a python package to generate various masks from the landsat 8 Quality Assessment band.

## Installation

The package can be shipped to your computer using pip.

	pip install pymasker

Or just install it with the source code.

	python setup.py install

This package depends on [**numpy**](http://www.numpy.org/). If you want to load the band file directly, [**GDAL**](https://pypi.python.org/pypi/GDAL/) is also in need.

## Sample

First of all, you need to load the QA band into the *qabmaser* class.
	
```python
from pymasker import qabmasker

# load the band file directly
masker = qabmasker(r'D:\LC80170302014272LGN00_BQA.TIF')

# load an numpy array that contains band data.
masker = qabmasker(bandarray)
```

The QA band contains the detection result of the following four specific conditions for each pixel:

* Cloud
* Cirrus
* Snow/Ice
* Vegetation
* Water body

For each condition, the algorithm gives a confidence to indicate its existence on the pixel.

```python
from pymasker import confidence

# Algorithm has high confidence that this condition exists (67-100 percent confidence).
conf = confidence.high

# Algorithm has medium confidence that this condition exists (34-66 percent confidence).
conf = confidence.medium

# Algorithm has low to no confidence that this condition exists (0-33 percent confidence)
conf = confidence.low

# Algorithm did not determine the status of this condition.
conf = confidence.undefined

# Nothing, unspecified confidence
conf = confidence.none
```

To generate a mask, you need to define a desired confidence for the target condition. 

*Pymasker* provides several functions to get the most commonly used mask. The resulting mask is a binary numpy array with 1 representing existence of specific condition and 0 representing nonexistence.

```python
# Get mask indicating cloud pixels with high confidence 
# (excluding cirrus)
mask = masker.getcloudmask(confidence.high)

# Get mask indicating cloud pixels with high confidence 
# (including cirrus)
mask = masker.getcloudmask(confidence.high, cirrus = True)

# Get mask indicating cloud pixels with at least medium confidence 
# (including cirrus)
mask = masker.getcloudmask(confidence.medium, cirrus = True, cumulative = True)

# Get mask indicating snow/ice pixels with at least medium confidence
mask = masker.getsnowmask(confidence.medium, cumulative = True)

# Get mask indicating water body pixels with high confidence
mask = masker.getwatermask(confidence.high)

# Get mask indicating vegetation pixels with high confidence
mask = masker.getvegmask(confidence.high)
```

*Pymasker* also provides a function for multi-criteria masking. In this function, you need to specify the confidence level of each condition. If you don't want the function consider one of conditions, you need to set it as confidence.none. Two different masking methods are provided:

* Inclusive	-	Mask pixels that meet at least one of all criteria.
* Exclusive	-	Only Mask pixels that meet all criteria. (default)

Sample code for multi-criteria masking

```python
# Get mask indicating cloud pixels (high confidence) and cirrus pixels (high confidence).
# Exclusive and noncumulative
mask = masker.getmask(cloud = confidence.high, cirrus = confidence.high)

# Save the result if you want.
masker.savetif(mask, r'D:\result.tif')
```

![Result](http://haoliangyu.net/images/GIS/masking-pymasker/maskresult.png)

Now you have your mask! Nice and quick!
