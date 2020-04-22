from PIL import Image
from src.data_struct.frame_data import FrameData
from src.functions.func import *
from src.constants.variables import *
from src.functions.bcolors import FAIL, ENDC
import cv2


def motion_capt(vid_var):
    """
    Performs the Motion Capture replacing the Monkey with red pixels
    :param vid_var: Variables of the video
    :return: If there is no problem, 0 is returned as well as the list with all the Frame Data objects
    and the grid size
    """
    # Calculate the size of the grid
    grid_size = set_grid(HEIGHT, WIDTH, MAX_GRID, MIN_GRID)
    if grid_size == -1:  # Check for errors
        print(FAIL + "[Error] wrong grid_size in motion_capt" + ENDC)
        return -1

    # List with all the frame objects
    if not test:
        length = vid_var[0] - 2
    else:
        length = test_val
    frame_list = get_frame_data(grid_size, length + 1)
    if frame_list is None:  # Check for errors
        print(FAIL + "[Error] wrong frame_list in motion_capt" + ENDC)
        return -1

    # Create folder for the Motion Capture Frames
    create_folder(MOTION_F)

    # Substitute the Monkey with red pixels
    start_progress("Replacing the Monkey with red pixels")

    for i in range(length):
        progress((i / length) * 100)
        monkey_to_red(frame_list[i], i)
    end_progress()

    # Create the video with the Motion Capture
    create_folder(MOTION_V_F)
    create_video(vid_var[2], vid_var[1], length, MOTION_V_F + MOTION_V, [MOTION_F + MOTION_N, MOTION_T])

    # Calculate the SSD and the displacement
    print("Calculating the Displacement:")
    for i in range(length):
        frame_list[i].disp = calculate_ssd(frame_list[i], frame_list[i + 1], grid_size)
    return 0, grid_size, frame_list


def monkey_to_red(frame, count):
    """
    Change the monkey to red pixels
    :param frame: Actual frame used for the replacement
    :param count: Number of the actual frame
    :return: The image with the Monkey as red pixels
    """
    # Image as Numpy Array
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, FRAME_F + frame.name)
    data = cv2.imread(filename)
    # Gray
    gray = rgb2gray(data)
    # Binary Threshold
    thresh = to_binary(gray, 50, 255)
    # Erode the background
    kernel = np.ones((5, 5), np.uint8)
    thresh = dilate_erode(thresh, kernel, 'erosion')

    # Mark in red the Monkey
    data[np.where((thresh == [0, 0, 0]).all(axis=2))] = [0, 33, 166]
    # Save Image
    img = Image.fromarray(bgr2rgb_np(data), 'RGB')
    img.save(dirname + "/" + MOTION_F + MOTION_N + '%d' % count + MOTION_T)
    return img


def get_frame_data(grid_size, length):
    """
    :param grid_size: Size of the grid used in the image
    :param length: Duration of the video
    :return: The list with all the FrameData objects of the video
    """
    start_progress("Creating the FrameData objects")
    frame_list = []
    for i in range(length):
        progress((i / length) * 100)
        # Default name for the frames
        name = FRAME_F + FRAME_N + '%d' % i + FRAME_T
        # Read the current frame
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, name)
        frame = cv2.imread(filename)
        if frame is None:  # Check for errors
            print(FAIL + "[Error] Cannot read image %s in main" % filename + ENDC)
            return None
        # Get the grid_map of the frame as well as the number of columns and rows of it
        img_map, row, column = grid_map(frame, grid_size)  # img_map[Y][X]
        frame_list.append(FrameData(name, img_map, frame, None))  # Add the new FrameData
    end_progress()
    return frame_list
