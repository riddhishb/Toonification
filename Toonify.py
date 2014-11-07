import cv2
import numpy as np 
import math
from matplotlib import pyplot as plt


def nothing(x):
	pass

input_image = cv2.imread('7.png')
cv2.imshow('Input Image',input_image)

#cv2.namedWindow('Toonified Image')
#cv2.createTrackbar('Iterations','Toonified Image',0,15,nothing)
#cv2.createTrackbar('colorquant value','Toonified Image',0,50,nothing)
#cv2.createTrackbar('Canny Threshold','Toonified Image',0,100,nothing)
#Phase 1 : color staircasing #########################################################################################################

# Then We Do Bilateral Filtering with k1 = kernal size and N = number of iterations
# We do Median Filtering
# Color quantization floor factor = a

#N = cv2.getTrackbarPos('Iterations','Toonified Image')
N=5
#a = cv2.getTrackbarPos('colorquant value','Toonified Image')
a= 24

for x in range(0,N):
	bilateral_filtimg = cv2.bilateralFilter(input_image,9,75,75)

median_filtimg = cv2.medianBlur(bilateral_filtimg,5)

[rows,cols,c] = median_filtimg.shape
colorquantimg = median_filtimg
for i in xrange(0,rows):
	for j in xrange(0,cols):
		xb = median_filtimg.item(i,j,0)
		xg = median_filtimg.item(i,j,1)
		xr = median_filtimg.item(i,j,2)  
		xb = math.floor(xb/a)*a 
		xg = math.floor(xg/a)*a
		xr = math.floor(xr/a)*a
		colorquantimg.itemset((i,j,0),xb)
		colorquantimg.itemset((i,j,1),xg)
		colorquantimg.itemset((i,j,2),xr)

#cv2.imshow('Phase1 output',colorquantimg)		

# Phase2 : Edge Extraction ############################################################################################################

# Appy Median Filter to the image 
# Canny Edge Detection
# Dialation of the detected edges
# Edgefilter
p=60
#p = cv2.getTrackbarPos('Canny Threshold','Toonified Image')

median_filtimg2 = cv2.medianBlur(input_image,5)

edges = cv2.Canny(median_filtimg2,p,2*p)
dialateimg =  cv2.dilate(edges,np.ones((3,3),'uint8'))
edges_inv = cv2.bitwise_not(dialateimg)
ret,thresh = cv2.threshold(edges_inv,127,255,0)
#cv2.imshow('edges',thresh)
contours, hierarchy = cv2.findContours(thresh,1,2)
img_contours = cv2.drawContours(thresh, contours, -1, (0,0,0), 3)
print img_contours
#cv2.imshow('counters',img_contours)

############################### Recombine both the images ##############################################################################
finalimg = colorquantimg
for i in xrange(0,rows):
	for j in xrange(0,cols):
		if edges_inv.item(i,j) == 0:
			finalimg.itemset((i,j,0),0)
			finalimg.itemset((i,j,1),0)
			finalimg.itemset((i,j,2),0)
cv2.imshow('Toonified Image',finalimg)
cv2.waitKey(0)
