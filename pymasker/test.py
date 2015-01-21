import sys
sys.path.append('D:\\Projects\\Python\\pymasker\\pymasker')

import gdal
from pymasker import qabmasker
from pymasker import confidence

bandfile = gdal.Open(r'C:\Users\Yu\Desktop\LC80170302014272LGN00_BQA.TIF')
qabband = bandfile.GetRasterBand(1).ReadAsArray()

masker = qabmasker(qabband)
masker.bandfile = bandfile
mask = masker.getmask(cloud=confidence.high, cirrus = confidence.high, inclusive = True)
masker.savetif(mask, r'C:\Users\Yu\Desktop\\test.tif')