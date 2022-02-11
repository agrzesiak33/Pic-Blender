from __future__ import print_function
import os
import cv2 as cv
import numpy as np

import helper


merge_whole = helper.PicMerge()
merge_whole.load_pics('pics')
merge_whole.set_main_width(2000)
#  merge_whole.correct_camera_movement(153)
# helper.save_image(merge_whole.pics[0], 'out1')
# helper.save_image(merge_whole.pics[1], 'out2')
merge_whole.whole_image_blend()
helper.save_image(merge_whole.blended_pic, 'out')
"""

merge_middle = helper.PicMerge()
merge_middle.load_pics('middle pics')
merge_middle.set_main_width(20)
merge_middle.set_blended_image_width(merge_middle.BLENDED_WIDTH+33)
merge_middle.middle_only_blend()
helper.save_image(merge_middle.blended_pic, 'out')
"""
