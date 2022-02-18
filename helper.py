import numpy as np
import cv2 as cv
import os
import configparser as cp


class PicMerge:
    def __init__(self):
        self.WIDTH = -1
        self.HEIGHT = -1
        self.BLENDED_WIDTH = -1
        self.BLENDED_HEIGHT = -1
        # Main widths are, in all cases, are inclusive on both ends
        self.main_widths = []
        self.main_locations = []
        self.NUM_PICS = -1
        self.blended_pic = []
        self.pics = []
        self.out_name = ''
        self.blend_type = ''

        # TODO add a non linear gradient...don't think this will work
        # TODO add logic to deal with differnet main widths

    def load_pics(self, filename):
        files = os.listdir(filename)
        self.NUM_PICS = len(files)
        if self.NUM_PICS == 0:
            return -1
        for file in range(self.NUM_PICS):
            self.pics.append(cv.imread(cv.samples.findFile(f"{filename}/{files[file]}")))
        self.WIDTH = len(self.pics[0][0])
        self.HEIGHT = len(self.pics[0])
        self.BLENDED_WIDTH = self.WIDTH
        self.BLENDED_HEIGHT = self.HEIGHT

        # By default, it will make the output image as large as one imported image
        self.blended_pic = np.zeros((self.HEIGHT, self.WIDTH, 3), np.uint8)

    def set_blended_image_width(self, width):
        self.blended_pic = np.zeros((self.HEIGHT, width, 3), np.uint8)
        self.BLENDED_WIDTH = width

    def set_main_width(self, main_width):
        self.main_widths = main_width

    """
    @ Brief
        Adds in the main column from source pic to the blended image
    @ Params
        [from_pic] : The input picture to add to the blended image
        [start_column] : The index where we will start adding columns in the blended image.  Inclusive
        [end_column] : The index where we will end adding columns in the blended image.  Also inclusive
        [src_start] : (Optional) The left index of the the source picture.  If this is provided it means the columns
                        we're adding to the blended image have a different start indexes. 
    """

    def transfer_main_columns(self, from_pic, start_column, end_column, src_start=-1):
        print('Transferring main cols')
        if end_column >= self.BLENDED_WIDTH:
            end_column = self.BLENDED_WIDTH - 1
        height = len(from_pic)
        current_src_col = src_start
        if current_src_col == -1:
            current_src_col = start_column

        for current_col in range(start_column, end_column + 1):
            for current_row in range(height):
                self.blended_pic[current_row][current_col] = np.uint8(from_pic[current_row][current_src_col])
            current_src_col += 1

    """
    @ Brief
        Takes a pic to add to the blended image and applies a gradient proportional to how many columns are between 
        the start and stop
    @ Params
        [pic] : The input picture to add to the blended image
        [right_start] : The index where we will start adding columns in the blended image.  Inclusive
        [left_stop] : The index where we will end adding columns in the blended image.  Also inclusive
        [src_start] : (Optional) The left index of the the source picture.  If this is provided it means the columns
                        we're adding to the blended image have a different start indexes. 
    """

    def add_gradient_left(self, pic, right_start, left_stop, src_left_start=-1):
        print('Adding gradient left')
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

        while current_col >= left_stop and total_gradient >= 0:
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

    """
    @ Brief
        Takes a pic to add to the blended image and applies a gradient proportional to how many columns are between 
        the start and stop
    @ Params
        [pic] : The input picture to add to the blended image
        [left_start] : The index where we will start adding columns in the blended image.  Inclusive
        [right_start] : The index where we will end adding columns in the blended image.  Also inclusive
        [src_right] : (Optional) The left index of the the source picture.  If this is provided it means the columns
                        we're adding to the blended image have a different start indexes. 
    """

    def add_gradient_right(self, pic, left_start, right_stop, src_right_start=-1):
        print('Adding Gradient right')
        # Get percentage of gradient per columns
        gradient_step = 100 / (right_stop - left_start)
        # Get decimal version of the percent
        gradient_step /= 100

        height = len(pic)
        total_gradient = 1
        current_col = left_start

        current_src_col = src_right_start
        if current_src_col == -1:
            current_src_col = current_col

        while current_col <= right_stop and total_gradient >= 0:
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

    # Only works for 2 images
    def correct_camera_movement(self, num_pixels):
        # I'm too drunk to understand why this works but it needs to multiply by 2 TODO
        num_pixels = int(num_pixels * 2)

        original_width = self.WIDTH

        if self.NUM_PICS != 2:
            exit(-1)
        else:
            self.blended_pic = self.blended_pic = np.zeros((self.HEIGHT, self.WIDTH + num_pixels, 3), np.uint8)

            left_image = np.zeros((self.HEIGHT, self.WIDTH + int((num_pixels / 2)), 3), np.uint8)
            right_image = np.zeros((self.HEIGHT, self.WIDTH + int((num_pixels / 2)), 3), np.uint8)

            self.WIDTH += int(num_pixels / 2)

            for col in range(0, original_width):
                for current_row in range(self.HEIGHT):
                    left_image[current_row][col] = np.uint8(self.pics[0][current_row][col])

            original_col = 0
            for col in range((int(num_pixels / 2)), self.WIDTH):
                for current_row in range(self.HEIGHT):
                    right_image[current_row][col] = np.uint8(self.pics[1][current_row][original_col])
                original_col += 1

            self.pics[0] = left_image
            self.pics[1] = right_image

    def whole_image_blend(self):
        # Make sure all images are the same size
        for pic in self.pics:
            if len(pic[0]) != self.WIDTH or len(pic) != self.HEIGHT:
                print('Not all images are the same size')
                exit(-1)

        main_locations = [[0, self.main_widths[0] - 1]]
        # Get all the middle main column locations
        for pic in range(1, len(self.pics) - 1):
            # Width of the current main column
            width = self.main_widths[pic]
            width += width % 2
            location = self.main_locations[pic]
            main_locations.append([location - int(width / 2) - 1, location + int(width / 2) - 1])
        # Get the last main column locations
        main_locations.append([self.WIDTH - self.main_widths[-1], self.WIDTH - 1])

        # Just helper variables to help readability
        left = 0
        right = 1
        for current_pic_index in range(self.NUM_PICS):
            # Transferring the main columns will be ubiquitous with any pic being added
            self.transfer_main_columns(self.pics[current_pic_index], main_locations[current_pic_index][left],
                                       main_locations[current_pic_index][right])
            # Do first things
            if current_pic_index == 0:
                print('Processing the first image')
                self.add_gradient_right(self.pics[current_pic_index], main_locations[current_pic_index][right] + 1,
                                        main_locations[current_pic_index + 1][left] - 1)

            # Do last things
            elif current_pic_index == self.NUM_PICS - 1:
                print('Processing the last image')
                self.add_gradient_left(self.pics[current_pic_index], main_locations[current_pic_index][left] - 1,
                                       main_locations[current_pic_index - 1][right] + 1)

            # Do normal things
            else:
                print(f'Processing the {current_pic_index + 1}th image')
                self.add_gradient_right(self.pics[current_pic_index], main_locations[current_pic_index][right] + 1,
                                        main_locations[current_pic_index + 1][left] - 1)
                self.add_gradient_left(self.pics[current_pic_index], main_locations[current_pic_index][left] - 1,
                                       main_locations[current_pic_index - 1][right] + 1)

    # TODO make this work list version of main widths
    """
    @ Brief
        Takes all the pictures and the main  slice meta-data from the config file and splices the different locations
        from each source picture and blends it together.  The output blended image will not be a 
    """

    def middle_only_blend(self):
        #  I want the main width to be even so the math is easier
        if self.main_widths % 2 != 0:
            self.main_widths += 1

        variable_main_widths = True
        if isinstance(self.main_widths, int):
            variable_main_widths = False

        main_locations = []
        if variable_main_widths:
            main_locations.append([0, self.main_widths[0] - 1])
            normalized_main_width = self.WIDTH / (len(self.pics) - 1)
            current_normal = normalized_main_width
            # Get all the middle main column locations
            for pic in range(1, len(self.pics) - 1):
                # Width of the current main column
                width = self.main_widths[pic]
                width += width % 2
                main_locations.append([current_normal - (width / 2) - 1, current_normal + (width / 2) - 1])
            # Get the last main column locations
            main_locations.append([self.WIDTH - self.main_widths[-1], self.WIDTH - 1])

        SLICE_BLEND_WIDTH = self.BLENDED_WIDTH - (self.NUM_PICS * self.main_widths)  # Get all non-main image area
        SLICE_BLEND_WIDTH /= (self.NUM_PICS - 1)  # There are NUM_PICS-1 blend areas
        SLICE_BLEND_WIDTH = round(SLICE_BLEND_WIDTH)

        # Make sure there are enough pixels on each image to blend
        room_to_blend = (self.WIDTH - self.main_widths) / 2
        if room_to_blend < SLICE_BLEND_WIDTH:
            return -1

        #  These pointers are only used to keep track of where we are in the blended image  #
        left_main_index_col = 0  # The left most main column of the image we're working on
        right_main_index_col = self.main_widths - 1  # The right mose main column of the image
        left_blend_index_col = -  1  # The column the gradients will be applied to when going left
        # ^^^^^^^^^^^DOESN'T GET USED UNTIL AFTER FIRST PIC IS PROCESSED
        right_blend_index_col = self.main_widths + SLICE_BLEND_WIDTH  # The column the gradient will be applied going right

        #  These pointers are only used to see where we're pulling pixels from in the original images
        left_source_main = int((self.WIDTH / 2) - (self.main_widths / 2))
        right_source_main = left_source_main + self.main_widths - 1  # The -1 is because the front and end index are inclusive

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
                save_image(self.blended_pic, 'out')
                self.add_gradient_left(self.pics[current_pic_index], left_main_index_col - 1,
                                       left_blend_index_col, left_source_main - 1)
                save_image(self.blended_pic, 'out')
                self.add_gradient_right(self.pics[current_pic_index], right_main_index_col + 1,
                                        right_blend_index_col, right_source_main + 1)

            left_blend_index_col = right_main_index_col + 1
            left_main_index_col = right_blend_index_col + 1
            right_main_index_col = left_main_index_col + self.main_widths - 1
            right_blend_index_col = right_main_index_col + SLICE_BLEND_WIDTH

    def load_config(self, config_filename, pic_folder):
        config = cp.ConfigParser()
        config.read(config_filename)

        self.load_pics(pic_folder)
        self.out_name = config['general']['out name']

        # This will work for now TODO
        if 's' in config.get(['general']['type']).lower():

            # If you want variable main widths
            if config.getboolean(['general']['variable main widths']):
                # Use self.main_width to hold a list with many widths
                self.main_widths = []
                main_widths = config.options('main widths')
                for main_width in main_widths:
                    self.main_widths.append(config.getint('main widths', main_width))
            # If all the widths are the same
            else:
                main_width = config.getint('general', 'main width')
                for pic in range(len(self.pics)):
                    self.main_widths.append([main_width])

            # If you want variable main locations
            if config.getboolean('general', 'variable main locations'):
                self.main_locations = []
                main_locations = config.options('main locations')
                for main_location in main_locations:
                    location = config.get('main locations', main_location)
                    if 'start' in location:
                        self.main_locations.append(0)
                    elif 'end' in location:
                        self.main_locations.append(self.WIDTH - 1)
                    else:
                        self.main_locations.append(int(location))
            else:
                main_offset = int(self.WIDTH / (len(self.pics) - 1))
                current_offset = 0
                self.main_locations = []
                for pic in range(len(self.pics) - 1):
                    self.main_locations.append(current_offset)
                    current_offset += main_offset
                self.main_locations.append(self.WIDTH - 1)


def display_image(pic):
    cv.imshow('dst', pic)
    cv.waitKey(0)
    cv.destroyAllWindows()


def save_image(pic, name):
    cv.imwrite(f'pics/{name}.png', pic)
