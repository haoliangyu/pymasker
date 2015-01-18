import gdal
import numpy as np
from enum import IntEnum

class confidence(IntEnum):
	'''Represents levels of confidence that a condition exists

 	yes 		-	Algorithm has high confidence that this condition exists (67-100 percent confidence).
 	maybe 		-	Algorithm has medium confidence that this condition exists (34-66 percent confidence).
 	no 			-	Algorithm has low to no confidence that this condition exists (0-33 percent confidence)
    undefine	- 	Algorithm did not determine the status of this condition.
	'''
	yes = 3
	maybe = 2
	no = 1
	undefine = 0

class masker:
	'''Provides access to functions that produces masks from quality assessment band of Landsat 8'''

	def __init__(self, filepath):
		self.load(filepath)

	def load(self, filepath):
		'''Load the BQA band from a give path

		Parameters
			filepath	-	Path of band file.
		'''
		self.bandfile = gdal.Open(filepath)
		self.bqaband = self.bandfile.GetRasterBand(1).ReadAsArray()

	def getcloudmask(self, conf, cirrus = True, cumulative = False):
		'''Generate a cloud mask.

		Parameters
			conf		-	Level of confidence that cloud exists.
			cirrus		-	A value indicating whether the mask includes cirrus.
			cumulative	-	A boolean value indicating whether the masking is cumulative.

		Return
			mask 		-	A two-dimension binary mask.
		'''
		if cirrus:
			return self.getmask(conf, conf, confidence.undefine, confidence.undefine, cumulative)
		else:
			return self.getmask(conf, confidence.undefine, confidence.undefine, confidence.undefine, cumulative)

	def getwatermask(self, conf, cumulative = False):
		'''Generate a water body mask.

		Parameters
			conf		-	Level of confidence that water body exists.
			cumulative	-	A boolean value indicating whether the masking is cumulative.

		Return
			mask 		-	A two-dimension binary mask.
		'''
		return self.getmask(confidence.undefine, confidence.undefine, confidence.undefine, conf, cumulative)			

	def getsnowmask(self, conf, cumulative = False):
		'''Generate a water body mask.

		Parameters
			conf		-	Level of confidence that snow/ice exists.
			cumulative	-	A boolean value indicating whether the masking is cumulative.

		Return
			mask 		-	A two-dimension binary mask.
		'''
		return self.getmask(confidence.undefine, confidence.undefine, conf, confidence.undefine, cumulative)	

	def getmask(self, cloud, cirrus, snow, water, cumulative = False):
		'''Get mask with given conditions.

		Parameters
			cloud		-	Level of confidence that cloud exists.
			cirrus		-	Level of confidence that cirrus exists.
			snow		-	Level of confidence that snow/ice exists.
			water		-	Level of confidence that water body exists.
			occluded	-	A value indicating whether it is terrain occluded.
			frame		-	A value indicating whether it is dropped frame.
			filled		-	A value indicating whether it is filled.
			cumulative	-	A boolean value indicating whether the masking is cumulative.

		Returns
			mask 		-	A two-dimension binary mask.
		'''

		# # Filled pixel
		# posValue = 1 << 0
		# conValue = int(filled) << 0
		# mask = (self.bqaband & posValue) == conValue

		# # Frame pixel
		# posValue = 1 << 1
		# conValue = int(frame) << 1
		# mask = mask | ((self.bqaband & posValue) == conValue)

		# # Terrain occluded pixel
		# posValue = 1 << 2
		# conValue = int(frame) << 2
		# mask = mask | ((self.bqaband & posValue) == conValue)

		# Temporary
		mask = self.bqaband < 0

		# Water body pixel
		if water != confidence.undefine:
			mask = mask | self.__masking(4, 3, int(water), cumulative)

		# Snow pixel
		if snow != confidence.undefine:
			mask = mask | self.__masking(10, 3, int(snow), cumulative)

		# Cirrus pixel
		if cirrus != confidence.undefine:
			mask = mask | self.__masking(12, 3, int(cirrus), cumulative)

		# Cloud pixel
		if cloud != confidence.undefine:
			mask = mask | self.__masking(14, 3, int(cloud), cumulative)

		return mask.astype(int)

	def __masking(self, bitloc, bitlen, value, cumulative):
		''''Get mask with specific parameters.

		Parameters
			bitloc		-	Location of the specific QA bits in the value string.
			bitlen		-	Length of the specific QA bits.
			value  		-	A value indicating the desired condition.
			cumulative	-	A boolean value indicating whether the masking is cumulative.
		'''
		posValue = bitlen << bitloc
		conValue = value << bitloc

		if cumulative:
			return ((self.bqaband & posValue) >= conValue)
		else:	
			return ((self.bqaband & posValue) == conValue)

	def save(self, mask, filepath):
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