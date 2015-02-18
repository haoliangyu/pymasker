import os
import numpy as np

class masker:
	'''Provides access to functions that produces masks from remote sensing image, according to its bit structure.'''

	def __init__(self, band, *var):
		
		if type(band) is str:
			if len(var) > 0:
				self.loadfile(band, var[0])
			else:
				self.loadfile(band)
		else:
			self.loadarray(band)

	def loadfile(self, filename, bandnum = 0):
		'''Load the QA file from a give path

		Parameters
			filename	-	Path of band file.
			bandnum		-	Number of band.
		'''
		import gdal

		self.filename = filename
		extension = os.path.splitext(filename)[1].lower()

		# load file according to the file format.
		if extension == '.hdf':		
			dataset = gdal.Open(filename)
			subdataset = dataset.GetSubDatasets()[bandnum][0]
			self.bandarray = gdal.Open(subdataset).ReadAsArray()
		else:
			bandfile = gdal.Open(filename)
			self.bandarray = bandfile.GetRasterBand(1).ReadAsArray()

	def loadarray(self, array):
		'''Load the BQA ban from a np.array

		Parameters
			array		-	Numpy array that contains the band data. 
		'''
		self.filename = None
		self.bandarray = array

	def getmask(self, bitpos, bitlen, value):
		'''Generates mask with given bit information.

		Parameters
			bitpos		-	Position of the specific QA bits in the value string.
			bitlen		-	Length of the specific QA bits.
			value  		-	A value indicating the desired condition.
		'''
		lenstr = ''
		for i in range(bitlen):
			lenstr += '1'
		bitlen = int(lenstr, 2)

		if type(value) == str:
			value = int(value, 2)

		posValue = bitlen << bitpos
		conValue = value << bitpos
		mask = (self.bandarray & posValue) == conValue

		return mask.astype(int)

	def savetif(self, mask, filepath):
		'''Save the given mask as a .tif file.

		Parameters
			mask 		-	A mask generated with masker.
			filepath	-	Path of .tif file.
		'''
		import gdal	

		driver = gdal.GetDriverByName('GTiff')

		x_pixels = mask.shape[1]
		y_pixels = mask.shape[0] 

		dataset = driver.Create(filepath, x_pixels, y_pixels, 1, gdal.GDT_Int32)

		if self.filename is not None:
			extension = os.path.splitext(self.filename)[1].lower()
			if extension == '.hdf':
				hdfdataset = gdal.Open(self.filename)
				subdataset = hdfdataset.GetSubDatasets()[0][0]
				bandfile = gdal.Open(subdataset)
			else:
				print('s')
				bandfile = gdal.Open(self.filename)

			dataset.SetGeoTransform(bandfile.GetGeoTransform())
			dataset.SetProjection(bandfile.GetProjectionRef())
			
		dataset.GetRasterBand(1).WriteArray(mask)
		dataset.FlushCache()
