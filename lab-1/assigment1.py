# In[0]
# Read the video and store the frames of it
import FrameData
from functions import *  # Functions used
import matplotlib.pyplot as plt

# Get the frames of the video
videoVariables = list(video_to_frames(constant.FRAME_SAVE_PATH, constant.PATH_TO_VIDEO))
# Variables of the video and of the frames
video_length = videoVariables[0]
height = int(videoVariables[1])
width = int(videoVariables[2])

# Calculate the size of the grid
grid_size = set_grid(height, width, constant.MAX_GRID, constant.MIN_GRID)
if grid_size == -1:  # Check for errors
    print(bcolors.FAIL + "[Error] wrong grid_size in assignment1" + bcolors.ENDC)
    exit(-1)

# In[1]
# Read all the frames of the video and get the Frame object of each one
# The Frame object has the grid_map, name and its original picture

# List with all the frame objects
frame_list = []
for i in range(2):
    # Default name for the frames
    name = constant.FRAME_PREFIX + '%d' % i + constant.FRAME_EXT
    # Read the current frame
    frame = cv2.imread(constant.FRAME_SAVE_PATH + name)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    if frame is None:  # Check for errors
        print(bcolors.FAIL + "[Error] Cannot read image %s in main" % (constant.FRAME_SAVE_PATH + name) + bcolors.ENDC)
        exit(-1)
    # Get the grid_map of the frame as well as the number of columns and rows of it
    img_map, row, column = grid_map(frame, grid_size)  # img_map[Y][X]
    frame_object = FrameData.FrameData(name, img_map, frame)
    frame_list.append(frame_object)

# In[2]
# Calculate the SSD and the displacement
# Draw the arrows of the displacement
# Draw the borders of the object
for i in range(1):
    # Calculate displacement
    disp = calculate_ssd(frame_list[i], frame_list[i + 1], grid_size)
    transform = frame_list[i].r_img
    # Draw the arrows
    for y_axis in range(len(disp) - 1):
        for x_axis in range(len(disp[0]) - 1):
            x_dest = int(disp[y_axis][x_axis][0] * grid_size)
            x_origin = int(disp[y_axis][x_axis][1] * grid_size)
            y_dest = int(disp[y_axis][x_axis][2] * grid_size)
            y_origin = int(disp[y_axis][x_axis][3] * grid_size)
            if x_dest != x_origin or y_dest != y_origin:
                transform = arrowdraw(transform, x_dest, y_dest, x_origin, y_origin)
    new_name = constant.TRANSFORM_PATH + constant.FRAME_PREFIX + '%d' % i + constant.FRAME_EXT
    # Frame with the arrows
    transform = cv2.cvtColor(transform, cv2.COLOR_BGR2RGB)

    # Draw the border of the object
    # Read the current frame
    name = constant.FRAME_PREFIX + '%d' % i + constant.FRAME_EXT
    frame = cv2.imread(constant.FRAME_SAVE_PATH + name)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Turn it to grey scale
    imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Threshold
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    # Get the contours of the image
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(transform, contours, -1, (255, 255, 255), 1)
    # Write image with the arrows and the contours

    # plt.figure(1)
    # plt.imshow(transform, cmap='gray')
    # plt.show()

    cv2.imwrite(new_name, transform)
    print()
