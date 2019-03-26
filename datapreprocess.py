from __future__ import print_function
from functools import reduce

import sys
import os
import numpy as np
import cv2
import math
import SimpleITK as sitk
import skimage.io as io
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

def read_img(path):
        reader = sitk.ImageFileReader()
        reader.SetImageIO("NiftiImageIO")
        reader.SetFileName(path)
        data = reader.Execute()
	return data


def img_show(img):
	for i in range(img.shape[0]):
		io.imshow(img[i,:,:],cmap='gray')
		print(i)
		io.show()


def img_store(img,outpath):
	#out = sitk.GetImageFromArray(img)
	writer = sitk.ImageFileWriter()
	writer.SetFileName(outpath)
	writer.Execute(img)
	#sitk.WriteImage(out,outpath)


def binary_mask(img):
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			for k in range(img.shape[2]):
				if img[i,j,k] > 0:
					img[i,j,k] = 255
	return img


def biasFieldCorrection(img,shrink):
	numberFittingLevels = 4
	inputImage = sitk.ReadImage(img,sitk.sitkFloat32)
	maskImage = sitk.OtsuThreshold(inputImage,0,1,200)
	inputImage = sitk.Shrink(inputImage,[int(shrink)]* inputImage.GetDimension())
	maskImage = sitk.Shrink(maskImage, [int(shrink)] * inputImage.GetDimension() )
	inputImage = sitk.Cast(inputImage, sitk.sitkFloat32)
	corrector = sitk.N4BiasFieldCorrectionImageFilter();
	output = corrector.Execute(inputImage, maskImage)

	return output

#delete labeled voxel(skull strip)
'''
path1 = ''#your file
img1 = read_img(path1)
path2 = ''#your label
img2 = read_img(path2)
img2 = sitk.GetArrayFromImage(img2)
outpath = ''
isize = img1.GetSize()
for i in range(isize[0]):
	for j in range(isize[1]):
		for k in range(isize[2]):
			if img2[k,j,i] == 0:
				img1.SetPixel(i,j,k,0)
#img_show(img1)
img_store(img1,outpath)
'''


#biasFieldCorrection

path = ''#corrected file
outpath = ''#skull striped file
shrink = 1
img = biasFieldCorrection(path,shrink)		
#img_show(output)
img_store(img,outpath)

