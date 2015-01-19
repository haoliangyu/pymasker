import gdal
import numpy as np

class confidence():
	'''Represents levels of confidence that a condition exists

 	high 		-	Algorithm has high confidence that this condition exists (67-100 percent confidence).
 	medium 		-	Algorithm has medium confidence that this condition exists (34-66 percent confidence).
 	low 		-	Algorithm has low to no confidence that this condition exists (0-33 percent confidence)
    undefined	- 	Algorithm did not determine the status of this condition.
	'''
	high = 3
	medium = 2
	low = 1
	undefined = 0

class qabmasker:
	'''Provides access to functions that produces masks from quality assessment band of Landsat 8'''

	def __init__(self, filepath):
		self.load(filepath)

	def load(self, filepath):
		'''Load the BQA band from a give path

		Parameters
			filepath	-	Path of band file.
		'''
		self.bandfile = gdal.Open(filepath)
		self.qaband = self.bandfile.GetRasterBand(1).ReadAsArray()

	def getcloudmask(self, conf, cirrus = True, cumulative = False):
		'''Generate a cloud mask.

		Parameters
			conf		-	Level of confidence that cloud exists.
			cirrus		-	A value indicating whether the mask includes cirrus.
			cumulative	-	A boolean value indicating whether the masking is cumulative.

		Return
			mask 		-	A two-dimension binary mask.
		'''

		mask = self.__masking(14, 3, conf, cumulative)

		if cirrus:
			mask = self.__masking2(msk, 12, 3, conf, False, cumulative)

		return mask.astype(int)

	def getvegmask(self, conf, cumulative = False):
		'''Generate a vegetation mask.

		Parameters
			conf		-	Level of confidence that vegetation exists.
			cumulative	-	A boolean value indicating whether the masking is cumulative.

		Return
			mask 		-	A two-dimension binary mask.
		'''
		return self.__masking(8, 3, conf, cumulative).astype(int)

	def getwatermask(self, conf, cumulative = False):
		'''Generate a water body mask.

		Parameters
			conf		-	Level of confidence that water body exists.
			cumulative	-	A boolean value indicating whether the masking is cumulative.

		Return
			mask 		-	A two-dimension binary mask.
		'''
		return self.__masking(4, 3, conf, cumulative).astype(int)

	def getsnowmask(self, conf, cumulative = False):
		'''Generate a water body mask.

		Parameters
			conf		-	Level of confidence that snow/ice exists.
			cumulative	-	A boolean value indicating whether the masking is cumulative.

		Return
			mask 		-	A two-dimension binary mask.
		'''
		return self.__masking(10, 3, conf, cumulative).astype(int)

	def getmask(self, cloud, cirrus, snow, vegetation, water, inclusive = False, cumulative = False):
		'''Get mask with given conditions.

		Parameters
			cloud		-	Level of confidence that cloud exists.
			cirrus		-	Level of confidence that cirrus exists.
			snow		-	Level of confidence that snow/ice exists.
			water		-	Level of confidence that water body exists.
			inclusive	-	A boolean value indicating whether the masking is inclusive or exclusive.
			cumulative	-	A boolean value indicating whether the masking is cumulative.

		Returns
			mask 		-	A two-dimension binary mask.
		'''

		# Basic mask
		if inclusive:
			mask = self.qaband < 0
		else:
			mask = self.qaband >= 0

		# Vegetation pixel
		mask = self.__masking2(mask, 8, 3, vegetation, cumulative, inclusive)

		# Snow pixel
		mask = self.__masking2(mask, 10, 3, snow, cumulative, inclusive)

		# Cirrus pixel
		mask = self.__masking2(mask, 12, 3, cirrus, cumulative, inclusive)

		# Cloud pixel
		mask = self.__masking2(mask, 14, 3, cloud, cumulative, inclusive)

		# Water body pixel
		mask = self.__masking2(mask, 4, 3, water, cumulative, inclusive)

		return mask.astype(int)

	def __masking(self, bitloc, bitlen, value, cumulative):
		'''Get mask with specific parameters.

		Parameters
			bitloc		-	Location of the specific QA bits in the value string.
			bitlen		-	Length of the specific QA bits.
			value  		-	A value indicating the desired condition.
			cumulative	-	A boolean value indicating whether the masking is cumulative.
		'''

		posValue = bitlen << bitloc
		conValue = value << bitloc

		if cumulative:
			mask = (self.qaband & posValue) >= conValue
		else:
			mask = (self.qaband & posValue) == conValue	
		
		return mask	

	def __masking2(self, basemask, bitloc, bitlen, value, cumulative, inclusive):
		''''Get mask with specific parameters.

		Parameters
			basemask	-	
			bitloc		-	Location of the specific QA bits in the value string.
			bitlen		-	Length of the specific QA bits.
			value  		-	A value indicating the desired condition.
			inclusive	-	A boolean value indicating whether the masking is inclusive or exclusive.
			cumulative	-	A boolean value indicating whether the masking is cumulative.
		'''

		mask = self.__masking(bitloc, bitlen, value, cumulative)

		if inclusive:
			return np.logical_or(basemask, mask)
		else:
			return np.logical_and(basemask, mask)

	def savetif(self, mask, filepath):
		'''Save the given mask as a .tif file.

		Parameters
			mask 		-	A mask generated with masker.
			filepath	-	Path of .tif file.
		'''

		driver = gdal.GetDriverByName('GTiff')

		x_pixels = mask.shape[1]
		y_pixels = mask.shape[0] 

		dataset = driver.Create(filepath, x_pixels, y_pixels, 1, gdal.GDT_Int32)
		dataset.SetGeoTransform(self.bandfile.GetGeoTransform())
		dataset.SetProjection(self.bandfile.GetProjectionRef())
		dataset.GetRasterBand(1).WriteArray(mask)
		dataset.FlushCache()