import numpy as np
import cv2
import sys


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
    # Check if the video has been opened correctly
    if not cap.isOpened():
        print('{} not opened'.format(path_video))
        sys.exit(1)

    # Variables of the video
    time_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    array = [time_length, frame_height, frame_width]

    frame_counter = 0  # FRAME_COUNTER
    while 1:
        return_flag, frame = cap.read()
        # If the flag is false the video has finished
        if not return_flag:
            print('Video Reach End')
            break
        cv2.imwrite(path_frame + 'frame%d.tif' % frame_counter, frame)
        frame_counter += 1

        if cv2.waitKey(30) & 0xff == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return array


# Convert an image to grey scale
def img_to_grey(img):
    # Step1: Convert to greyscale if required
    img_grey = np.zeros(img.shape[:2])
    for row_idx in range(img.shape[0]):
        for col_idx in range(img.shape[1]):
            rgb_components = img[row_idx][col_idx]
            img_grey[row_idx][col_idx] = int(0.212670 * rgb_components[0] +0.715160 * rgb_components[1] + 0.072169 * rgb_components[2])
    # print('Converted Image Shape:', img_grey.shape)
    return img_grey


def save_grey(origin_path, dest_path):
    """
    Converts the images of the origin path to a grey and saves them into the destination path
    :param origin_path: The folder containing the frames to convert
    :param dest_path:  Destination folder
    """
    frame_counter = 0  # FRAME_COUNTER
    aux = 49
    while 1:
        img = cv2.imread(origin_path + 'frame%d.tif' % aux)
        # If the flag is false the video has finished
        if img is None or aux == 93:  # Read only the ball images
            print('Image reading to the end')
            break
        # Convert the image to grey
        grey_img = img_to_grey(img)
        cv2.imwrite(dest_path + 'frame_grey%d.tif' % frame_counter, grey_img)
        frame_counter += 1
        aux += 1


def save_threshold(origin_path, dest_path, intensity):
    """
    Converts the images of the origin path to a threshold and saves them into the destination path
    :param origin_path: The folder containing the frames to convert
    :param dest_path:  Destination folder
    :param intensity:  Intensity used in the threshold function
    """
    frame_counter = 0  # FRAME_COUNTER
    while 1:
        img = cv2.imread(origin_path + 'frame_grey%d.tif' % frame_counter)
        # If the flag is false the video has finished
        if img is None:
            print('Image reading to the end')
            break
        ret, thresh_img = cv2.threshold(img, intensity, 255, cv2.THRESH_TOZERO)
        cv2.imwrite(dest_path + 'frame_thresh%d.tif' % frame_counter, thresh_img)
        frame_counter += 1


def calculate_mean(path):
    img = cv2.imread(path)
    processed_img = np.zeros(img.shape)
    counter = 0
    mean = [0, 0]
    for row_idx in range(processed_img.shape[0]):
        for col_idx in range(processed_img.shape[1]):
            # Search for the pixels different to 0 (Black) and store its values
            if img[row_idx, col_idx, 0] != 0:
                counter += 1
                mean = [(row_idx + mean[0]), (col_idx + mean[1])]
    #
    mean = [(mean[0] / counter, (mean[1]) / counter)]
    return [int(mean[0][0]), int(mean[0][1])]

