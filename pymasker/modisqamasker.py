import numpy as np

from masker import masker

class modisquality():
	'''Level of data quality of MODIS land products at each pixel.

	high		-	Corrected product produced at ideal quality for all bands.
	medium		-	Corrected product produced at less than ideal quality for some or all bands.
	low 		-	Corrected product not produced due to some reasons for some or all bands.
	low_cloud	-	Corrected product not produced due to cloud effects for all bands.
	'''

	high = 0,
	medium = 1,
	low = 2,
	low_cloud = 3

class modisqamasker(masker):
	'''Provides access to functions that produce QA masks from quality assessment band of MODIS land products.'''

	def getqamask(self, quality):
		'''Get a quality mask.

		Parameters
			quality		-	Desired level of data quality.

		Returns
			mask 		-	A two-dimension binary mask.
		'''

		return self.getmask(0, 2, quality).astype(int)