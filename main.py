from __future__ import print_function
import os
import cv2 as cv
import numpy as np

import helper

"""
merge_whole = helper.PicMerge()
merge_whole.load_pics('pics')
merge_whole.set_main_width(10)
merge_whole.whole_image_blend()
helper.save_image(merge_whole.blended_pic, 'out')
"""

merge_middle = helper.PicMerge()
merge_middle.load_pics('middle pics')
merge_middle.set_main_width(10)
merge_middle.middle_only_blend()
helper.save_image(merge_middle.blended_pic, 'out')

