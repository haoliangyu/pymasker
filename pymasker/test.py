import sys
sys.path.append('D:\\Projects\\Python\\pymasker\\pymasker')

import gdal
from pymasker import landsatmasker
from pymasker import confidence
from pymasker import masker

# *************************************************************************** #
#                             Landsat Test                  
# *************************************************************************** #
bandfile = gdal.Open(r'D:\Documents\University Course\SUNY Buffalo\GEO653 Advanced Remote Sensing\Project\Data\Clipped Image\BQA_Clipped.TIF')
qabband = bandfile.GetRasterBand(1).ReadAsArray()

masker = landsatmasker(qabband)
masker.bandfile = bandfile
mask = masker.getmultimask(cloud=confidence.high, cirrus = confidence.high, inclusive = True)
masker.savetif(mask, r'C:\Users\Yu\Desktop\\test6.tif')

# *************************************************************************** #
#                               Modis Test                  
# *************************************************************************** #
# bandfile = 'C:\\Users\\Yu\Desktop\\MOD09GQ.A2014274.h11v05.005.2014279025826.hdf'
# bandnum = 3

# masker = masker(bandfile, bandnum)
# mask = masker.getmask(13, 1, '1')
# masker.savetif(mask, r'C:\Users\Yu\Desktop\\test4.tif')