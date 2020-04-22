import constant
from functions import video_to_frames, img_to_grey, save_threshold, save_grey, calculate_mean
import sys
import cv2
from matplotlib import pyplot as plt


# In[1]
# Extract frame from video and save them in folder
# videoVariables = list(video_to_frames(constant.FRAME_SAVE_PATH, constant.PATH_TO_VIDEO))


# In[2]
# Frames to grey
# save_grey(constant.FRAME_SAVE_PATH, constant.GREY_SAVE_PATH)


# In[3]
# Pixel intensity threshold of the ball
# save_threshold(constant.GREY_SAVE_PATH, constant.THRESHOLD_SAVE_PATH, 250)

# In[4]
# Calculate the mean coordinate for the ball
mean = calculate_mean("./threshold/frame_thresh3.tif")
print(mean)


