from __future__ import print_function
import os
import cv2 as cv
import numpy as np

import helper

HEIGHT = -1
WIDTH = -1
NUM_PICS = -1
SLICE_MAIN_WIDTH = 10
ALPHA = -1
BETA = -1

pics = []
# Get input from user where the pictures are
#print('Enter folder name')
input_folder = 'pics'
#input_folder = input().strip()

files = os.listdir(input_folder)

if files.__sizeof__() == 0:
    print('No files found')
    exit(-1)

for file in range(len(files)):
    pics.append(cv.imread(cv.samples.findFile(f"{input_folder}/{files[file]}")))

# Ensure all images are the same size
NUM_PICS = len(pics)
WIDTH = len(pics[0][0])
HEIGHT = len(pics[0])
for pic in pics:
    if len(pic[0]) != WIDTH or len(pic) != HEIGHT:
        print('Not all images are the same size')
        exit(-1)

SLICE_BLEND_WIDTH = WIDTH - (NUM_PICS * SLICE_MAIN_WIDTH) - 1  # Get all non-main image area
SLICE_BLEND_WIDTH /= (NUM_PICS - 1)  # There are NUM_PICS-1 blend areas
SLICE_BLEND_WIDTH = round(SLICE_BLEND_WIDTH)

# Final image
blended_image = np.zeros((HEIGHT, WIDTH, 3), np.uint8)

left_main_index_col = 0  # The left most main column of the image we're working on
right_main_index_col = SLICE_MAIN_WIDTH - 1  # The right mose main column of the image
left_blend_index_col = -  1  # The column the gradients will be applied to when going left
# ^^^^^^^^^^^DOESN'T GET USED UNTIL AFTER FIRST PIC IS PROCESSED
right_blend_index_col = SLICE_MAIN_WIDTH + SLICE_BLEND_WIDTH  # The column the gradient will be applied going right

for current_pic_index in range(len(pics)):
    # Do first things
    if current_pic_index == 0:
        helper.transfer_main_columns(pics[current_pic_index], blended_image, left_main_index_col, right_main_index_col + 1)
        helper.add_gradient_right(pics[current_pic_index], blended_image, right_main_index_col + 1, right_blend_index_col + 1)

    # Do last things
    elif current_pic_index == NUM_PICS - 1:
        helper.transfer_main_columns(pics[current_pic_index], blended_image, left_main_index_col, right_main_index_col + 1)
        helper.add_gradient_left(pics[current_pic_index], blended_image, left_main_index_col - 1, left_blend_index_col)

    # Do normal things
    else:
        helper.transfer_main_columns(pics[current_pic_index], blended_image, left_main_index_col, right_main_index_col + 1)
        helper.add_gradient_left(pics[current_pic_index], blended_image, left_main_index_col - 1, left_blend_index_col)
        helper.add_gradient_right(pics[current_pic_index], blended_image, right_main_index_col + 1, right_blend_index_col)

    left_blend_index_col = right_main_index_col + 1
    left_main_index_col = right_blend_index_col + 1
    right_main_index_col = left_main_index_col + SLICE_MAIN_WIDTH - 1
    right_blend_index_col = right_main_index_col + SLICE_BLEND_WIDTH

helper.save_image(blended_image, 'out')
