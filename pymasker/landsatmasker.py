import numpy as np

from masker import masker

class confidence():
	'''Levels of confidence that a condition exists

 	high 		-	Algorithm has high confidence that this condition exists (67-100 percent confidence).
 	medium 		-	Algorithm has medium confidence that this condition exists (34-66 percent confidence).
 	low 		-	Algorithm has low to no confidence that this condition exists (0-33 percent confidence)
    undefined	- 	Algorithm did not determine the status of this condition.
    none		-	Nothing.
	'''
	high = 3
	medium = 2
	low = 1
	undefined = 0
	none = -1

class landsatmasker(masker):
	'''Provides access to functions that produces masks from quality assessment band of Landsat 8.'''

	def getcloudmask(self, conf, cirrus = True, cumulative = False):
		'''Generate a cloud mask.

		Parameters
			conf		-	Level of confidence that cloud exists.
			cirrus		-	A value indicating whether the mask includes cirrus.
			cumulative	-	A Boolean value indicating whether the masking is cumulative.

		Return
			mask 		-	A two-dimension binary mask.
		'''

		mask = self.__masking(14, 3, conf, cumulative)

		if cirrus:
			mask = self.__masking2(mask, 12, 3, conf, False, cumulative)

		return mask.astype(int)

	def getvegmask(self, conf, cumulative = False):
		'''Generate a vegetation mask.

		Parameters
			conf		-	Level of confidence that veg exists.
			cumulative	-	A Boolean value indicating whether the masking is cumulative.

		Return
			mask 		-	A two-dimension binary mask.
		'''
		return self.__masking(8, 3, conf, cumulative).astype(int)

	def getwatermask(self, conf, cumulative = False):
		'''Generate a water body mask.

		Parameters
			conf		-	Level of confidence that water body exists.
			cumulative	-	A Boolean value indicating whether the masking is cumulative.

		Return
			mask 		-	A two-dimension binary mask.
		'''
		return self.__masking(4, 3, conf, cumulative).astype(int)

	def getsnowmask(self, conf, cumulative = False):
		'''Generate a water body mask.

		Parameters
			conf		-	Level of confidence that snow/ice exists.
			cumulative	-	A Boolean value indicating whether the masking is cumulative.

		Return
			mask 		-	A two-dimension binary mask.
		'''
		return self.__masking(10, 3, conf, cumulative).astype(int)

	def getmultimask(self, 
			        cloud = confidence.none, cloud_cum = False, 
			        cirrus = confidence.none, cirrus_cum = False,
			        snow = confidence.none, snow_cum = False, 
			        veg = confidence.none, veg_cum = False,
			        water = confidence.none, water_cum = False,
			        inclusive = False):
		'''Get mask with multiple conditions.

		Parameters
			cloud		-	Level of confidence that cloud exists. (default: confidence.none)
			cloud_cum	-	A Boolean value indicating whether the cloud masking is cumulative.
			cirrus		-	Level of confidence that cirrus exists. (default: confidence.none)
			cirrus_cum	-	A Boolean value indicating whether the cirrus masking is cumulative. (default: False)
			snow		-	Level of confidence that snow/ice exists. (default: confidence.none)
			snow_cum 	-	A Boolean value indicating whether the snow masking is cumulative. (default: False)
			veg			-	Level of confidence that vegetation exists. (default: confidence.none)
			veg_cum		-	A Boolean value indicating whether the vegetation masking is cumulative. (default: False)
			water		-	Level of confidence that water body exists. (default: confidence.none)
			water_cum	-	A Boolean value indicating whether the water body masking is cumulative. (default: False)
			inclusive	-	A Boolean value indicating whether the masking is inclusive or exclusive.

		Returns
			mask 		-	A two-dimension binary mask.
		'''

		# Basic mask
		if inclusive:
			mask = self.bandarray < 0
		else:
			mask = self.bandarray >= 0

		# veg pixel
		mask = self.__masking2(mask, 8, 3, veg, veg_cum, inclusive)

		# Snow pixel
		mask = self.__masking2(mask, 10, 3, snow, snow_cum, inclusive)

		# Cirrus pixel
		mask = self.__masking2(mask, 12, 3, cirrus, cirrus_cum, inclusive)

		# Cloud pixel
		mask = self.__masking2(mask, 14, 3, cloud, cloud_cum, inclusive)

		# Water body pixel
		mask = self.__masking2(mask, 4, 3, water, water_cum, inclusive)

		return mask.astype(int)

	def __masking(self, bitloc, bitlen, value, cumulative):
		'''Get mask with specific parameters.

		Parameters
			bitloc		-	Location of the specific QA bits in the value string.
			bitlen		-	Length of the specific QA bits.
			value  		-	A value indicating the desired condition.
			cumulative	-	A Boolean value indicating whether the masking is cumulative.
		'''

		posValue = bitlen << bitloc
		conValue = value << bitloc

		if cumulative:
			mask = (self.bandarray & posValue) >= conValue
		else:
			mask = (self.bandarray & posValue) == conValue	
		
		return mask	

	def __masking2(self, basemask, bitloc, bitlen, value, cumulative, inclusive):
		''''Get mask with specific parameters.

		Parameters
			basemask	-	Base mask.
			bitloc		-	Location of the specific QA bits in the value string.
			bitlen		-	Length of the specific QA bits.
			value  		-	A value indicating the desired condition.
			inclusive	-	A Boolean value indicating whether the masking is inclusive or exclusive.
			cumulative	-	A Boolean value indicating whether the masking is cumulative.
		'''

		if value == confidence.none:
			return basemask

		mask = self.__masking(bitloc, bitlen, value, cumulative)

		if inclusive:
			return np.logical_or(basemask, mask)
		else:
			return np.logical_and(basemask, mask)
