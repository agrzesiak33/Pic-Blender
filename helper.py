import numpy as np
import cv2 as cv


def transfer_main_columns(from_pic, blended_pic, start_column, end_column, src_start=-1):
    height = len(from_pic)
    current_src_col = src_start
    if current_src_col == -1:
        current_src_col = start_column

    for current_col in range(start_column, end_column):
        for current_row in range(height):
            blended_pic[current_row][current_col] = np.uint8(from_pic[current_row][current_src_col])
        current_src_col += 1


def add_gradient_left(pic, blended_pic, right_start, left_stop, src_left_start=-1):
    # Get percentage of gradient per column
    gradient_step = 100 / (right_start - left_stop)
    # Get decimal version of the percent
    gradient_step /= 100

    height = len(pic)
    total_gradient = 1
    current_col = right_start

    current_src_col = src_left_start
    if current_src_col == -1:
        current_src_col = current_col

    while current_col > left_stop and total_gradient >= 0:
        # Apply the gradient correction to all the pixels
        for current_row in range(height):
            pixel_to_add = pic[current_row][current_src_col]
            # Apply the gradient, round it, then convert it back to an 8-bit pixel
            pixel_to_add = [round(rgb * total_gradient) for rgb in pixel_to_add]

            # In case the pixel already had blending done to it, the gradient needs to be added
            for value in range(3):
                projected_rgb_value = blended_pic[current_row][current_col][value] + pixel_to_add[value]
                if projected_rgb_value > 255:
                    blended_pic[current_row][current_col][value] = 255
                else:
                    blended_pic[current_row][current_col][value] = np.uint8(projected_rgb_value)

        current_col -= 1
        current_src_col -= 1
        total_gradient -= gradient_step


def add_gradient_right(pic, blended_pic, left_start, right_stop, src_right_start=-1):
    # Get percentage of gradient per column
    gradient_step = 100 / (right_stop - left_start)
    # Get decimal version of the percent
    gradient_step /= 100

    height = len(pic)
    total_gradient = 1
    current_row = 0
    current_col = left_start

    current_src_col = src_right_start
    if current_src_col == -1:
        current_src_col = current_col

    while current_col < right_stop and total_gradient >= 0:
        # Apply the gradient correction to all the pixels
        for current_row in range(height):
            pixel_to_add = pic[current_row][current_src_col]
            # Apply the gradient, round it, then convert it back to an 8-bit pixel
            pixel_to_add = [round(rgb * total_gradient) for rgb in pixel_to_add]

            # In case the pixel already had blending done to it, the gradient needs to be added
            for value in range(3):
                projected_rgb_value = blended_pic[current_row][current_col][value] + pixel_to_add[value]
                if projected_rgb_value > 255:
                    blended_pic[current_row][current_col][value] = 255
                else:
                    blended_pic[current_row][current_col][value] = np.uint8(projected_rgb_value)
        current_src_col += 1
        current_col += 1
        total_gradient -= gradient_step


def display_image(pic):
    cv.imshow('dst', pic)
    cv.waitKey(0)
    # [display]
    cv.destroyAllWindows()


def save_image(pic, name):
    cv.imwrite(f'pics/{name}.png', pic)


def middle_only_blend(pics, blended_image, main_width):
    # Only takes the middle main_size of every image and blends left and right appropriately
    HEIGHT = len(pics[0])
    WIDTH = len(pics[0][0])
    NUM_PICS = len(pics)

    #  I want the main width to be even so the math is easier
    if main_width % 2 != 0:
        main_width += 1

    SLICE_BLEND_WIDTH = WIDTH - (NUM_PICS * main_width) - 1  # Get all non-main image area
    SLICE_BLEND_WIDTH /= (NUM_PICS - 1)  # There are NUM_PICS-1 blend areas
    SLICE_BLEND_WIDTH = round(SLICE_BLEND_WIDTH)

    # Make sure there are enough pixels on each image to blend
    room_to_blend = (WIDTH - main_width) / 2
    if room_to_blend < SLICE_BLEND_WIDTH:
        return -1

    #  These pointers are only used to keep track of where we are in the blended image  #
    left_main_index_col = 0  # The left most main column of the image we're working on
    right_main_index_col = main_width - 1  # The right mose main column of the image
    left_blend_index_col = -  1  # The column the gradients will be applied to when going left
    # ^^^^^^^^^^^DOESN'T GET USED UNTIL AFTER FIRST PIC IS PROCESSED
    right_blend_index_col = main_width + SLICE_BLEND_WIDTH  # The column the gradient will be applied going right

    #  These pointers are only used to see where we're pulling pixels from in the original images
    left_source_main = (WIDTH / 2) - (main_width / 2)
    right_source_main = left_source_main + main_width - 1  # The -1 is because the front and end index are inclusive

    return 1

