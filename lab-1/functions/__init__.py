import math
from typing import List
import numpy as np
import cv2
import sys
import constant
from functions.bcolors import FAIL, ENDC


def video_to_frames(path_frame, path_video):
    """
    Convert a video to frames
    :type path_frame: String
    :type path_video: String
    :argument path_frame: Path to the frame's folder
    :argument path_video: Path to the video
    :rtype: array with the three attributes of the video

    """
    # Extract frame from video and save them in folder
    cap = cv2.VideoCapture(path_video)
    if not cap.isOpened():  # Check if the video has been opened correctly
        print('{} not opened'.format(path_video))
        sys.exit(1)
    # Variables of the video
    time_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(time_length)
    frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

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
    array = [time_length, frame_height, frame_width]
    frame_counter = 0  # FRAME_COUNTER
    while 1:
        return_flag, frame = cap.read()
        # If the flag is false the video has finished
        if not return_flag:
            break
        # Resize the frames
        if resize:
            dim = (int(frame_width), int(frame_height))
            frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        new_name = path_frame + constant.FRAME_PREFIX + '%d' % frame_counter + constant.FRAME_EXT
        cv2.imwrite(new_name, frame)
        frame_counter += 1

        if cv2.waitKey(30) & 0xff == ord('q'):
            break
    print(frame_counter)
    cap.release()
    cv2.destroyAllWindows()
    return array


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
    for i in range(row):
        sys.stdout.write('.')  # Progress bar
        sys.stdout.flush()
        ssd_vector = []
        for j in range(column):
            # Calculate the SSD matrix for each block in the original frame
            ssd_array = ssd_block(frame1.bmap[i][j], frame2, j, i, grid_size)
            ssd_vector.append(ssd_array)
        ssd_matrix.append(ssd_vector)
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
    max_len = constant.MAXIMUM_NEIGHBOUR
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


def arrowdraw(img, x1, y1, x2, y2):
    radians = math.atan2(x1 - x2, y2 - y1)
    x11 = 0
    y11 = 0
    x12 = -5
    y12 = -5

    u11 = 0
    v11 = 0
    u12 = 5
    v12 = -5

    x11_ = x11 * math.cos(radians) - y11 * math.sin(radians) + x2
    y11_ = x11 * math.sin(radians) + y11 * math.cos(radians) + y2

    x12_ = x12 * math.cos(radians) - y12 * math.sin(radians) + x2
    y12_ = x12 * math.sin(radians) + y12 * math.cos(radians) + y2

    u11_ = u11 * math.cos(radians) - v11 * math.sin(radians) + x2
    v11_ = u11 * math.sin(radians) + v11 * math.cos(radians) + y2

    u12_ = u12 * math.cos(radians) - v12 * math.sin(radians) + x2
    v12_ = u12 * math.sin(radians) + v12 * math.cos(radians) + y2

    img = cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 4)
    img = cv2.line(img, (int(x11_), int(y11_)), (int(x12_), int(y12_)), (255, 0, 0), 4)
    img = cv2.line(img, (int(u11_), int(v11_)), (int(u12_), int(v12_)), (255, 0, 0), 4)
    return img


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
