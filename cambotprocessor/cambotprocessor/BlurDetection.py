import cv2
import os
from imutils import paths

def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus measure
	return cv2.Laplacian(image,cv2.CV_64F).var()

def remove_blur(imgDir,blur):
	blurryImages = []
	for imagePath in paths.list_images(imgDir):
		# load the image, convert it to grayscale, and compute the focus measure  
		image = cv2.imread(imagePath)
		grayImg = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		fm = variance_of_laplacian(grayImg)
		# if the focus measure is less than the supplied threshold, then the image should be thrown out the Dataset
		if fm > blur:
			print("image: " + imagePath + " is blurry")
			blurryImages.append(imagePath)
	#removes tagged images out of Dataset		
	for imagePath in blurryImages:
		os.remove(imagePath)
		print("image: " + imagePath + " has been removed")