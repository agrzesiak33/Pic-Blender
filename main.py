from __future__ import print_function
import os
import cv2 as cv
import numpy as np

import helper

HEIGHT = -1
WIDTH = -1
NUM_PICS = -1
SLICE_MAIN_WIDTH = 10

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

blended_image = np.zeros((HEIGHT, WIDTH, 3), np.uint8)


helper.save_image(blended_image, 'out')
