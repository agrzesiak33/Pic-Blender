import numpy as np
import cv2 as cv


def transfer_main_columns(from_pic, blended_pic, start_column, end_column):
    height = len(from_pic)
    current_row = 0
    for current_col in range(start_column, end_column):
        for current_row in range(height):
            blended_pic[current_row][current_col] = np.uint8(from_pic[current_row][current_col])


def add_gradient_left(pic, blended_pic, right_start, left_stop):
    # Get percentage of gradient per column
    gradient_step = 100 / (right_start - left_stop)
    # Get decimal version of the percent
    gradient_step /= 100

    height = len(pic)
    total_gradient = 1
    current_row = 0
    current_col = right_start

    while current_col > left_stop and total_gradient >= 0:
        #save_image(blended_pic, 'out')
        # Apply the gradient correction to all the pixels
        for current_row in range(height):
            pixel_to_add = pic[current_row][current_col]
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
        total_gradient -= gradient_step


def add_gradient_right(pic, blended_pic, left_start, right_stop):
    # Get percentage of gradient per column
    gradient_step = 100 / (right_stop - left_start)
    # Get decimal version of the percent
    gradient_step /= 100

    height = len(pic)
    total_gradient = 1
    current_row = 0
    current_col = left_start

    while current_col < right_stop and total_gradient >= 0:
        # Apply the gradient correction to all the pixels
        for current_row in range(height):
            pixel_to_add = pic[current_row][current_col]
            # Apply the gradient, round it, then convert it back to an 8-bit pixel
            pixel_to_add = [round(rgb * total_gradient) for rgb in pixel_to_add]

            # In case the pixel already had blending done to it, the gradient needs to be added
            for value in range(3):
                projected_rgb_value = blended_pic[current_row][current_col][value] + pixel_to_add[value]
                if projected_rgb_value > 255:
                    blended_pic[current_row][current_col][value] = 255
                else:
                    blended_pic[current_row][current_col][value] = np.uint8(projected_rgb_value)

        current_col += 1
        total_gradient -= gradient_step


def display_image(pic):
    cv.imshow('dst', pic)
    cv.waitKey(0)
    # [display]
    cv.destroyAllWindows()


def save_image(pic, name):
    cv.imwrite(f'pics/{name}.png', pic)
