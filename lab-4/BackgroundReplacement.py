# In[1]
# Package required and global variable declaration
import numpy as np
import sys
import cv2

BLUE_MAX = np.array([0, 0, 200], np.uint8)
BLUE_MIN = np.array([50, 50, 255], np.uint8)
path_to_video = './monkey.avi'


# In[6]
# Replace the blue pixels of the foreground image with the background
def replace_blue(background, foreground):
    (h, w, c) = foreground.shape
    processed_img = np.zeros((h, w))
    for row_idx in range(foreground.shape[0]):
        for col_idx in range(foreground.shape[1]):
            rgb_component = foreground[row_idx][col_idx]

            dets = cv2.inRange(rgb_component, BLUE_MIN, BLUE_MAX)
            if rgb_component < BLUE_MAX & rgb_component > BLUE_MIN:
                grey_value = rgb_component[0] * 0.212671 + 0.715160 * rgb_component[1] + 0.072169 * rgb_component[2]
                processed_img[row_idx][col_idx] = grey_value
    processed_img = np.uint8(processed_img)
    return processed_img


# In[2]
# Use cv2 to have access to video frame by frame
# Capture Video and represent it as a object
cap = cv2.VideoCapture(path_to_video)
# Check whether video is captured correctly by cv2
if not cap.isOpened():
    print('{} not opened'.format(path_to_video))
    sys.exit(1)
# Use cv2 to fetch three important variables
time_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# Use for loop to have access to video frame by frame
while (1):
    reture_flag, frame = cap.read()  # reture_flag=False when the video ends
    if not reture_flag:
        print('Video Reach End')
        break

    # Main Content - Start
    # cv2.imshow('VideoWindowTitle-Quadrangle', frame)
    # Main Content - End

    # cv2.waitKey(30) - delay for 30 milliseconds and return a value to indicate whether this step is successful
    # 0xff == ord('q') - out of scope of this course. Don't worry.
    if cv2.waitKey(30) & 0xff == ord('q'):
        break
# Securely release video and close windows
cap.release()
cv2.destroyAllWindows()

# In[4]
# Extract frame from video and save them in folder
frame_save_path = './PATHTOBACKGROUND/'

# In[5]
cap = cv2.VideoCapture(path_to_video)
if not cap.isOpened():
    print('{} not opened'.format(path_to_video))
    sys.exit(1)
time_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_counter = 0  # FRAME_COUNTER
while (1):
    reture_flag, frame = cap.read()
    if not reture_flag:
        print('Video Reach End')
        break

    # Main Content - Start

    # cv2.imshow('VideoWindowTitle-Quadrangle', frame)
    frame = replace_blue(frame, frame)
    cv2.imwrite(frame_save_path + 'frame%d.tif' % frame_counter, frame)
    frame_counter += 1

    # Main Content - End

    if cv2.waitKey(30) & 0xff == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

# In[7]
# Get the background video and merge both
path_to_video = './Quadrangle.mov'

cap = cv2.VideoCapture(path_to_video)
if not cap.isOpened():
    print('{} not opened'.format(path_to_video))
    sys.exit(1)
time_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_counter = 0  # FRAME_COUNTER
while (1):
    reture_flag, frame = cap.read()
    if not reture_flag:
        print('Video Reach End')
        break

    # Main Content - Start

    cv2.imshow('VideoWindowTitle-Quadrangle', frame)
    # cv2.imwrite(frame_save_path + 'frame%d.tif' % frame_counter, frame)
    frame_counter += 1

    # Main Content - End

    if cv2.waitKey(30) & 0xff == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
