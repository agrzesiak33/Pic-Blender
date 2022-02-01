from __future__ import print_function
import os
import cv2 as cv
import numpy as np

import helper

HEIGHT = -1
WIDTH = -1
NUM_PICS = -1
SLICE_MAIN_WIDTH = 100 #TODO
SLICE_BLEND_WIDTH = 40 #TODO
ALPHA = -1
BETA = -1

pics = []
# Get input from user where the pictures are
print('Enter folder name')
input_folder = input().strip()

files = os.listdir(input_folder)

if files.__sizeof__() == 0:
    print('No files found')
    exit(-1)

for file in range(len(files)):
    pics.append(cv.imread(cv.samples.findFile(f'{input_folder}/{files[i]}')))

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

# Final image
blended_image = np.zeros((WIDTH, HEIGHT, 3), np.uint8)

left_main_index_col = 0 # The left most main column of the image we're working on
right_main_index_col = SLICE_MAIN_WIDTH #The right mose main column of the image
left_blend_index_col = SLICE_MAIN_WIDTH # The column the gradients will be applied to when going left
right_blend_index_col = SLICE_MAIN_WIDTH + SLICE_BLEND_WIDTH # The column the gradient will be applied going right

for current_pic_index in range(len(pics)):
    # Do first things
    if current_pic_index == 0:
        helper.transfer_main_columns(pics[current_pic_index], blended_image, left_main_index_col, right_main_index_col)
        helper.add_gradient_right(pics[current_pic_index], blended_image, right_main_index_col, right_blend_index_col)

    # Do last things
    elif current_pic_index == NUM_PICS - 1:
        helper.transfer_main_columns(pics[current_pic_index], blended_image, left_main_index_col, right_main_index_col)
        helper.add_gradient_left(pics[current_pic_index], blended_image, left_main_index_col, left_blend_index_col)

    # Do normal things
    else:
        helper.transfer_main_columns(pics[current_pic_index], blended_image, left_main_index_col, right_main_index_col)
        helper.add_gradient_left(pics[current_pic_index], blended_image, left_main_index_col, left_blend_index_col)
        helper.add_gradient_left(pics[current_pic_index], blended_image, right_main_index_col, right_blend_index_col)

    left_main_index_col = right_blend_index_col + 1
    right_main_index_col = left_main_index_col + SLICE_MAIN_WIDTH
    left_blend_index_col = left_main_index_col - SLICE_BLEND_WIDTH
    right_blend_index_col = right_main_index_col + SLICE_BLEND_WIDTH



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
