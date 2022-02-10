import numpy as np
import cv2 as cv
import os


class PicMerge:
    def __init__(self):
        self.WIDTH = -1
        self.HEIGHT = -1
        self.BLENDED_WIDTH = -1
        self.BLENDED_HEIGHT = -1
        self.main_width = -1
        self.NUM_PICS = -1
        self.blended_pic = []
        self.pics = []

    def load_pics(self, filename):
        files = os.listdir(filename)
        self.NUM_PICS = len(files)
        if self.NUM_PICS == 0:
            return -1
        for file in range(self.NUM_PICS):
            self.pics.append(cv.imread(cv.samples.findFile(f"{filename}/{files[file]}")))
        self.WIDTH = len(self.pics[0][0])
        self.HEIGHT = len(self.pics[0])

        # By default, it will make the output image as large as one imported image
        self.blended_pic = np.zeros((self.HEIGHT, self.WIDTH, 3), np.uint8)

    def set_blended_image_size(self, height, width):
        self.blended_pic = np.zeros((height, width, 3), np.uint8)
        self.BLENDED_HEIGHT = height
        self.BLENDED_WIDTH = width

    def set_main_width(self, main_width):
        self.main_width = main_width

    def transfer_main_columns(self, from_pic, start_column, end_column, src_start=-1):
        height = len(from_pic)
        current_src_col = src_start
        if current_src_col == -1:
            current_src_col = start_column

        for current_col in range(start_column, end_column):
            for current_row in range(height):
                self.blended_pic[current_row][current_col] = np.uint8(from_pic[current_row][current_src_col])
            current_src_col += 1

    def add_gradient_left(self, pic, right_start, left_stop, src_left_start=-1):
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
                    projected_rgb_value = self.blended_pic[current_row][current_col][value] + pixel_to_add[value]
                    if projected_rgb_value > 255:
                        self.blended_pic[current_row][current_col][value] = 255
                    else:
                        self.blended_pic[current_row][current_col][value] = np.uint8(projected_rgb_value)

            current_col -= 1
            current_src_col -= 1
            total_gradient -= gradient_step

    def add_gradient_right(self, pic, left_start, right_stop, src_right_start=-1):
        # Get percentage of gradient per column
        gradient_step = 100 / (right_stop - left_start)
        # Get decimal version of the percent
        gradient_step /= 100

        height = len(pic)
        total_gradient = 1
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
                    projected_rgb_value = self.blended_pic[current_row][current_col][value] + pixel_to_add[value]
                    if projected_rgb_value > 255:
                        self.blended_pic[current_row][current_col][value] = 255
                    else:
                        self.blended_pic[current_row][current_col][value] = np.uint8(projected_rgb_value)
            current_src_col += 1
            current_col += 1
            total_gradient -= gradient_step

    def whole_image_blend(self):
        for pic in self.pics:
            if len(pic[0]) != self.WIDTH or len(pic) != self.HEIGHT:
                print('Not all images are the same size')
                exit(-1)

        SLICE_BLEND_WIDTH = self.WIDTH - (self.NUM_PICS * self.main_width) - 1  # Get all non-main image area
        SLICE_BLEND_WIDTH /= (self.NUM_PICS - 1)  # There are NUM_PICS-1 blend areas
        SLICE_BLEND_WIDTH = round(SLICE_BLEND_WIDTH)

        left_main_index_col = 0  # The left most main column of the image we're working on
        right_main_index_col = self.main_width - 1  # The right mose main column of the image
        left_blend_index_col = -  1  # The column the gradients will be applied to when going left
        # ^^^^^^^^^^^DOESN'T GET USED UNTIL AFTER FIRST PIC IS PROCESSED
        right_blend_index_col = self.main_width + SLICE_BLEND_WIDTH  # The column the gradient will be applied going right

        for current_pic_index in range(self.NUM_PICS):
            # Do first things
            if current_pic_index == 0:
                self.transfer_main_columns(self.pics[current_pic_index], left_main_index_col,
                                           right_main_index_col + 1)
                self.add_gradient_right(self.pics[current_pic_index], right_main_index_col + 1,
                                        right_blend_index_col + 1)

            # Do last things
            elif current_pic_index == self.NUM_PICS - 1:
                self.transfer_main_columns(self.pics[current_pic_index], left_main_index_col,
                                           right_main_index_col + 1)
                self.add_gradient_left(self.pics[current_pic_index], left_main_index_col - 1,
                                       left_blend_index_col)

            # Do normal things
            else:
                self.transfer_main_columns(self.pics[current_pic_index], left_main_index_col,
                                           right_main_index_col + 1)
                self.add_gradient_left(self.pics[current_pic_index], left_main_index_col - 1,
                                       left_blend_index_col)
                self.add_gradient_right(self.pics[current_pic_index], right_main_index_col + 1,
                                        right_blend_index_col)

            left_blend_index_col = right_main_index_col + 1
            left_main_index_col = right_blend_index_col + 1
            right_main_index_col = left_main_index_col + self.main_width - 1
            right_blend_index_col = right_main_index_col + SLICE_BLEND_WIDTH

    def middle_only_blend(self):
        #  I want the main width to be even so the math is easier
        if self.main_width % 2 != 0:
            self.main_width += 1

        SLICE_BLEND_WIDTH = self.WIDTH - (self.NUM_PICS * self.main_width) - 1  # Get all non-main image area
        SLICE_BLEND_WIDTH /= (self.NUM_PICS - 1)  # There are NUM_PICS-1 blend areas
        SLICE_BLEND_WIDTH = round(SLICE_BLEND_WIDTH)

        # Make sure there are enough pixels on each image to blend
        room_to_blend = (self.WIDTH - self.main_width) / 2
        if room_to_blend < SLICE_BLEND_WIDTH:
            return -1

        #  These pointers are only used to keep track of where we are in the blended image  #
        left_main_index_col = 0  # The left most main column of the image we're working on
        right_main_index_col = self.main_width - 1  # The right mose main column of the image
        left_blend_index_col = -  1  # The column the gradients will be applied to when going left
        # ^^^^^^^^^^^DOESN'T GET USED UNTIL AFTER FIRST PIC IS PROCESSED
        right_blend_index_col = self.main_width + SLICE_BLEND_WIDTH  # The column the gradient will be applied going right

        #  These pointers are only used to see where we're pulling pixels from in the original images
        left_source_main = int((self.WIDTH / 2) - (self.main_width / 2))
        right_source_main = left_source_main + self.main_width - 1  # The -1 is because the front and end index are inclusive

        for current_pic_index in range(self.NUM_PICS):
            # Do first things
            if current_pic_index == 0:
                self.transfer_main_columns(self.pics[current_pic_index], left_main_index_col,
                                           right_main_index_col + 1, left_source_main)
                self.add_gradient_right(self.pics[current_pic_index], right_main_index_col + 1,
                                        right_blend_index_col + 1, right_source_main + 1)

            # Do last things
            elif current_pic_index == self.NUM_PICS - 1:
                self.transfer_main_columns(self.pics[current_pic_index], left_main_index_col,
                                           right_main_index_col + 1, left_source_main)
                self.add_gradient_left(self.pics[current_pic_index], left_main_index_col - 1,
                                       left_blend_index_col, left_source_main - 1)

            # Do normal things
            else:
                self.transfer_main_columns(self.pics[current_pic_index], left_main_index_col,
                                           right_main_index_col + 1, left_source_main)
                self.add_gradient_left(self.pics[current_pic_index], left_main_index_col - 1,
                                       left_blend_index_col, left_source_main - 1)
                self.add_gradient_right(self.pics[current_pic_index], right_main_index_col + 1,
                                        right_blend_index_col, right_source_main + 1)

            left_blend_index_col = right_main_index_col + 1
            left_main_index_col = right_blend_index_col + 1
            right_main_index_col = left_main_index_col + self.main_width - 1
            right_blend_index_col = right_main_index_col + SLICE_BLEND_WIDTH


def display_image(pic):
    cv.imshow('dst', pic)
    cv.waitKey(0)
    cv.destroyAllWindows()


def save_image(pic, name):
    cv.imwrite(f'pics/{name}.png', pic)
