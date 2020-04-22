import math
import cv2
from src.constants.variables import *
import numpy as np
from typing import List

from src.functions.auxiliary import *
from src.functions.bcolors import FAIL, ENDC


def find_common_divisors(a, b):
    """
    Returns the common divisors of two given numbers
    :param a: first value
    :param b: second value
    :return: list with the divisors of both numbers
    """
    n = 0
    nums: List[int] = []
    for i in range(1, min(a, b) + 1):
        if a % i == b % i == 0:
            nums.append(i)
            n += 1
    return nums


def set_grid(height, width, max_num, min_num):
    """
    Set the size of the grid giving a width and a height
    The size of the grid MUST be odd

    :type height: Int
    :type width: Int
    :type max_num: Int
    :type min_num: Int
    :argument height
    :argument width
    :argument max_num: maximum number of grids
    :argument min_num: minimum number of grids
    :rtype: int with the size of the grid. If there is any error, -1 is returned

    """
    # Get the divisors of the height and width
    divisors = find_common_divisors(height, width)
    candidates = []
    # Find the candidates for the grid size
    for item in divisors:
        x = width / item
        y = height / item
        aux = x * y
        # Check if it fulfils the conditions
        if (aux <= max_num) & (aux >= min_num):
            candidates.append(item)
    for candidate in candidates:
        if not candidate % 2 == 0:  # The grid must be odd
            return candidate
    return -1


def get_block(x, y, grid_size, img):
    """
    Giving an X & Y coordinate, it returns a list with the block corresponding to it
    :param x: X coordinate
    :param y: Y coordinate
    :param grid_size: Size of the Block
    :param img: Source Image
    :return: The list with the pixels of the corresponding block
    """
    if (x < 0) or y < 0:  # Check for correct values received
        print(FAIL + "[Error] Wrong coordinates to get_block()" + ENDC)
        return None
    # Block of pixels
    block = []
    # Origin point
    x_origin = ((x + 1) * grid_size) - grid_size
    y_origin = ((y + 1) * grid_size) - grid_size
    for i in range(grid_size):
        aux_block = []
        for j in range(grid_size):
            # Get the pixel
            aux_block.append(img[j + y_origin][i + x_origin])
        block.append(aux_block)
    return block


def grid_map(img, grid_size):
    """
    Creates the equivalent grid map of the given image
    :param img: Image to create the map from
    :param grid_size: The size of the grid
    """
    height, width, channels = img.shape
    column = int(width / grid_size)
    row = int(height / grid_size)
    if (width % grid_size != 0) or (height % grid_size != 0):  # Check that we have received the correct image size
        print(FAIL + "[Error] Wrong size of the input image at grid_map()" + ENDC)
    img_map = []
    for i in range(row - 1):
        # New row list
        row_map = []
        for j in range(column - 1):
            # Get the block of a given x,y of the Grid Map
            # We iterate through a row from left to right
            block = get_block(j, i, grid_size, img)
            if block is None:  # Check for errors getting the Block
                return None
            # Add a new element to the row list
            row_map.append(block)
        # Add the new row list to the Grid Map
        img_map.append(row_map)
    return img_map, row, column


def video_to_frames(path_frame, path_video):
    """
    Convert a video to frames
    :type path_frame: String
    :type path_video: String
    :argument path_frame: Path to the frame's folder
    :argument path_video: Path to the video
    :rtype: array with the three attributes of the video
    """
    # Create the folder that will contain the frames
    create_folder(path_frame)
    # Extract frame from video and save them in folder
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, path_video)
    cap = cv2.VideoCapture(filename)
    if not cap.isOpened():  # Check if the video has been opened correctly
        print('{} not opened'.format(filename))
        sys.exit(1)

    # Variables of the video
    time_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    start_progress("Converting Video to Frames")

    # Resize the video to have an odd dimensions
    resize = None
    # Check if we have to resize the video
    if int(frame_height) % 2 == 0 or int(frame_width) % 2 == 0:
        # Resize the video
        resize = True
        if frame_height % 2 == 0:
            aux = int(frame_height) % 3
            frame_height -= aux
        if frame_width % 2 == 0:
            aux = int(frame_width) % 3
            frame_width -= aux
    frame_counter = 0  # FRAME_COUNTER
    aux = 0  # FRAME_COUNTER
    dirname = os.path.dirname(__file__)
    while 1:
        progress((frame_counter / time_length) * 100)
        return_flag, frame = cap.read()
        # If the flag is false the video has finished
        if not return_flag:
            break
        # Resize the frames
        if resize:
            dim = (int(frame_width), int(frame_height))
            frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        new_name = path_frame + FRAME_N + '%d' % frame_counter + FRAME_T
        filename = os.path.join(dirname, new_name)
        cv2.imwrite(filename, frame)
        frame_counter += 1
        aux = aux + 1
    array = [frame_counter, frame_height, frame_width]
    cap.release()
    cv2.destroyAllWindows()
    end_progress()
    return array


def calculate_ssd(frame1, frame2, grid_size):
    """
    Calculates the ssd matrix for two given frames
    :param grid_size: size of the block
    :param frame1: first frame
    :param frame2: second frame
    """
    global ssd_vector
    column = len(frame1.bmap[0])
    row = len(frame1.bmap)
    ssd_matrix = []
    start_progress("\tSSD calculation of %s" % frame1.name)
    for i in range(row):
        progress((i / row) * 100)
        ssd_vector = []
        for j in range(column):
            # Calculate the SSD matrix for each block in the original frame
            ssd_array = ssd_block(frame1.bmap[i][j], frame2, j, i, grid_size)
            ssd_vector.append(ssd_array)
        ssd_matrix.append(ssd_vector)
    end_progress()
    return ssd_matrix


def ssd_block(origin_block, destination_frame, x, y, grid_size):
    """
    Receives the original block and the destination frame
    Calculates the SSD matrix for the given origin_block
    Returns the SSD matrix
    :param x: X coordinate of the origin_block
    :param y: Y coordinate of the origin_block
    :param origin_block: Bi
    :param destination_frame: F'i+1
    :param grid_size: size of the block
    :return: SSD matrix
    """
    # Starting point for checking for neighbours
    border_matrix = check_borders(x, y, len(destination_frame.bmap), len(destination_frame.bmap[0]))
    for item in border_matrix:
        if item == -1:  # Check correct values returned
            print(FAIL + "[Error] Wrong border matrix from ssd_block()" + ENDC)
            return None
    ssd = 9999
    disp = [x, x, y, y]  # Default values
    # Calculate the SSD value for each position
    for j in range(border_matrix[3] - border_matrix[2]):
        for i in range(border_matrix[1] - border_matrix[0]):
            # Check that we do not use the actual position
            if not (i == x and j == y):
                # Indexes
                y_aux = border_matrix[2] + j
                x_aux = border_matrix[0] + i
                # Get the new ssd value
                ssd_aux = ssd_formula(origin_block, destination_frame.bmap[y_aux][x_aux], grid_size)
                # Compare to know if the value is a new min
                if ssd_aux < ssd and not int(ssd_aux) == 0 and 190 < int(ssd_aux) < 210:
                    # Store the new ssd value and the displacement
                    ssd = ssd_aux
                    disp = [i + x, x, j + y, y]
    return disp


def check_borders(x, y, row, column):
    """
    :param x: X coordinate
    :param y: Y coordinate
    :param row: Number of rows of the map
    :param column: Number of columns of the map
    :return: an array with the following format:
    [x_origin, x_max, y_origin, y_max]
    x_origin meaning the starting neighbour of the to check
    x_max meaning the last neighbour of the to check
    """
    x_coord = check_axis(x, column)
    y_coord = check_axis(y, row)
    return [x_coord[0], x_coord[1], y_coord[0], y_coord[1]]


def check_axis(point, map_max):
    if point >= map_max or point < 0:
        return [-1, -1]
    # Maximum distance for a neighbour
    max_len = MAX_NEIGHBOUR
    # It goes out from the left axis
    if point - max_len - 1 < 0:
        origin = 0
        # It goes out from the right of the axis
        if point + max_len > map_max:
            last = map_max - 1 - origin
        # Goes out from the left but not the right in the axis
        else:
            last = point - origin + max_len
    # It only goes out from the right in the axis
    elif point + max_len >= map_max:
        origin = point - max_len
        last = map_max - 1 - origin
    # Base case of the axis
    else:
        origin = point - max_len
        last = (max_len * 2)
    return [origin, origin + last]


def ssd_formula(origin_block, destination_block, grid_size):
    """
    Receives two blocks to calculate the SSD Formula
    Returns the value of the calculation
    :param origin_block: Bi
    :param destination_block: B'i+1
    :param grid_size: size of the block
    :return: result of the calculation
    """
    ssd = 0
    for y in range(grid_size):
        for x in range(grid_size):
            # Go through all the pixels of the origin_block
            # Calculate the ssd value for all the combinations of the actual pixel
            # of the origin block with the pixels of the destination block
            ssd += np.sum((origin_block[y][x] - destination_block[0:grid_size][0:grid_size]) ** 2)
    return math.sqrt(ssd)


def dilate_erode(img_in, kernel, operation):
    """
    Performs the Dilation and Erosion operations
    :param img_in: Image used in the transformation
    :param kernel:  Kernel used for the transformation
    :param operation: Dilation or Erosion operation
    :return: The image transformed
    """
    assert operation == 'dilate' or operation == 'erosion'
    img = img_in[:, :, 0]
    final = np.zeros(img_in.shape)
    new_img = np.copy(img)

    kernel_size = kernel.shape[0]
    radius = int(kernel_size / 2)

    h, w = img.shape
    for x in range(radius, h - radius):
        for y in range(radius, w - radius):
            demo_array = img[x - radius: x + radius + 1, y - radius: y + radius + 1]
            if operation == 'dilate':
                result = np.amax(demo_array * kernel)
            else:
                result = np.amin(demo_array * kernel)
            new_img[x][y] = result

    final[:, :, 0] = new_img
    final[:, :, 1] = new_img
    final[:, :, 2] = new_img
    return final


def print_block(block):
    """
    Prints a block of pixels
    :param block:
    """
    for i in range(len(block)):
        msg = " "
        for j in range(len(block)):
            msg += str(block[j][i]) + ","
        print(msg)
    pass


def bgr2rgb_np(data):
    data_aux = data.copy()
    b, g, r = cv2.split(data_aux)  # get b,g,r
    rgb_np = cv2.merge([r, g, b])  # switch it to rgb
    return rgb_np


def rgb2gray(img):
    """
    Convert a RGB image to a Black and White image
    :param img: Input image in np
    :return: Black and White Image
    """
    img_grey = img.copy()
    img_new_grey = 0.212671 * img[:, :, 2] + 0.715160 * img[:, :, 0] + 0.072169 * img[:, :, 1]
    img_grey[:, :, 0] = img_new_grey
    img_grey[:, :, 1] = img_new_grey
    img_grey[:, :, 2] = img_new_grey
    return img_grey


def to_binary(gray, lower, upper):
    return ((gray > lower) + np.zeros(gray.shape)) * upper


# Find the object coordinate by averaging the foreground coordinates
def find_center(frame, threshold):
    xsum = 0
    ysum = 0
    ctr = 0

    for x in range(frame.shape[0]):
        for y in range(frame.shape[1]):
            if frame[x][y][2] > threshold:
                xsum += x
                ysum += y
                ctr += 1
    xmean = 0
    ymean = 0

    if ctr <= 20:
        xmean = -1
        ymean = -1
    else:
        xmean = xsum / ctr
        ymean = ysum / ctr

    return int(xmean), int(ymean)
