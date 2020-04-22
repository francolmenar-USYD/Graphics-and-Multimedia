# In[1]
# Package required and global variable declaration
import sys
import cv2
path_to_video = './Quadrangle.mov'

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
    cv2.imshow('VideoWindowTitle-Quadrangle', frame)
    # Main Content - End

    # cv2.waitKey(30) - delay for 30 milliseconds and return a value to indicate whether this step is successful
    # 0xff == ord('q') - out of scope of this course. Don't worry.
    if cv2.waitKey(30) & 0xff == ord('q'):
        break
# Securely release video and close windows
cap.release()
cv2.destroyAllWindows()

# In[3]
# A standard format to process video via cv2
cap = cv2.VideoCapture(path_to_video)
if not cap.isOpened():
    print('{} not opened'.format(path_to_video))
    sys.exit(1)
time_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
while (1):
    reture_flag, frame = cap.read()  # reture_flag=False when the video ends
    if not reture_flag:
        print('Video Reach End')
        break

    # Main Content - Start
    cv2.imshow('VideoWindowTitle-Quadrangle', frame)

    # Main Content - End

    if cv2.waitKey(30) & 0xff == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

# In[4]
# Extract frame from video and save them in folder
frame_save_path = './frames/'

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
    cv2.imshow('VideoWindowTitle-Quadrangle', frame)
    cv2.imwrite(frame_save_path + 'frame%d.tif' % frame_counter, frame)
    frame_counter += 1

    # Main Content - End

    if cv2.waitKey(30) & 0xff == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

# In[6]
# Output frames as one single video
frame_load_path = './frames/'
path_to_output_video = './new_video.mov'

# In[7]
out = cv2.VideoWriter(path_to_output_video, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (int(frame_width), int(frame_height)))
frame_counter = 0
while(1):
    img = cv2.imread(frame_load_path + 'frame%d.tif' % frame_counter)
    if img is None:
        print('No more frames to be loaded')
        break;
    out.write(img)
    frame_counter += 1
out.release()
cv2.destroyAllWindows()