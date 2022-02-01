from __future__ import print_function
import os
import cv2 as cv
import numpy as np
from os import listdir

HEIGHT = -1
WIDTH = -1
NUM_PICS = -1
SLICE_MAIN_WIDTH = 100 #TODO
SLICE_BLEND_WIDTH = 40 #TODO
SLICE_BLEND_GRADIENT = -1
ALPHA = -1
BETA = -1

pics = []
# Get input from user where the pictures are
print('Enter folder name')
input_folder = input().strip()

# Open all images and store in _pics_
files = os.listdir(input_folder)

if files.__sizeof__() == 0:
    print('No files found')
    exit(-1)

i = 0
for file in files:
    pics.append(cv.imread(cv.samples.findFile(f'{input_folder}/{files[i]}')))
    i += 1

# Ensure all images are the same size
NUM_PICS = len(pics)
WIDTH = len(pics[0][0])
HEIGHT = len(pics[0])
for pic in pics:
    if len(pic[0]) != WIDTH or len(pic) != HEIGHT:
        print('Not all images are the same size')
        exit(-1)

SLICE_BLEND_WIDTH = WIDTH - (NUM_PICS * SLICE_MAIN_WIDTH) #Get all non-main image area
SLICE_BLEND_WIDTH /= (NUM_PICS - 1) #There are NUM_PICS-1 blend areas
SLICE_BLEND_WIDTH = round(SLICE_MAIN_WIDTH)
# SLICE_BLEND_GRADIENT is the percentage each pixel will decrease by as the gradient filter is applied
SLICE_BLEND_GRADIENT = (100 / SLICE_BLEND_WIDTH) / 100

# Final image
blended = np.zeros((WIDTH, HEIGHT, 3), np.uint8)
pic_index = 0

for pic in pics:
    if pic_index == 0:
        # Do first things
        for
    elif pic_index == NUM_PICS:
        # Do last things
    else:
        # Do normal things

cv.imshow('pic', pics[1])
cv.waitKey(0)
# [display]
cv.destroyAllWindows()

"""print(''' Simple Linear Blender
-----------------------
* Enter alpha [0.0-1.0]: ''')
input_alpha = float(input().strip())
if 0 <= alpha <= 1:
    alpha = input_alpha
# [load]

# [load]
if src1 is None:
    print("Error loading src1")
    exit(-1)
elif src2 is None:
    print("Error loading src2")
    exit(-1)
# [blend_images]
beta = (1.0 - alpha)
dst = cv.addWeighted(src1, alpha, src2, beta, 0.0)
# [blend_images]
# [display]
cv.imshow('dst', dst)
cv.waitKey(0)
# [display]
cv.destroyAllWindows()
"""
