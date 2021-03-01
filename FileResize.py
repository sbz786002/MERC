import json
import io
import base64
from matplotlib import pyplot as plt
import numpy as np
import cv2
from PIL import Image
import pandas as pd

def image_resize(image, width, height, inter = cv2.INTER_AREA):
    dim = None
    if width is None and height is None:
        return image
    
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation = inter)
    return resized

def img_box(img1):
    loc=np.argwhere(img1==255)
    loc_x=list(loc[:,0])
    loc_y=list(loc[:,1])
    loc_z=list(loc[:,2])

    im=np.copy(img1)
    im[loc_x,loc_y,loc_z]=0

    im_a2=im.sum(axis=2)

    left_most=np.argwhere(im_a2.sum(axis=0)>0)[0][0]
    right_most=np.argwhere(im_a2.sum(axis=0)>0)[-1][0]

    upper_most=np.argwhere(im_a2.sum(axis=1)>0)[0][0]
    lower_most=np.argwhere(im_a2.sum(axis=1)>0)[-1][0]

    return img1[ upper_most:lower_most, left_most:right_most]

def main(fileimg,h,w):
	rd = "data:image/jpeg;base64,"
	img = fileimg
	heightst = int(h)
	widthst = int(w)
	# convert numpy array to image
	_c_width = widthst
	_c_height = heightst
	_canvas = np.ones((_c_width, _c_height, 3), np.uint8)
	_canvas.fill(255)
	my_string = base64.b64encode(img.read())
	im_bytes = base64.b64decode(my_string)
	im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
	img1 = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
	res = img_box(img1)
	diff = 0
	if res.shape[0] > _canvas.shape[0] or res.shape[1] > _canvas.shape[1]:
		x_diff = (res.shape[0] - _canvas.shape[0]) / res.shape[0]
		y_diff = (res.shape[1] - _canvas.shape[1]) / res.shape[1]
		diff = x_diff
		if y_diff > x_diff:
			diff = y_diff
	if diff > 0:
		diff = round(diff, 2) + .05
	resiz = image_resize(res,round(res.shape[1]*(1-diff)), round(res.shape[0]*(1-diff)))
	h, w = resiz[:,:,0].shape
	hh, ww = _canvas[:,:,0].shape
	yoff = round((hh - h) / 2)
	xoff = round((ww - w) / 2)
	result = _canvas.copy()
	result[yoff:yoff + h, xoff:xoff + w] = resiz
	image = base64.b64encode(cv2.imencode('.jpg', result)[1]).decode()

	return(rd+image)