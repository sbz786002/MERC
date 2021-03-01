import argparse
import cv2
from imutils import paths

def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

def main(imgpath):
	text = ''
	threshold = 50
	image = cv2.imread(imgpath)
	try:
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	except:
		return "Not Find"
	fm = variance_of_laplacian(gray)
	if fm > threshold:
		text = "Not Blurry: " + str(fm)
	if fm < threshold:
		text = "Blurry: " + str(fm)
	return text