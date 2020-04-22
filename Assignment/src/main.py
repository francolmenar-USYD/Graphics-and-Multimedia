# In[0]
from src.sections.intelligent_obj import create_objects
from src.sections.motion_capt import motion_capt
from src.functions.func import *
from src.sections.replace import replace, draw_stickman

from src.sections.sound import sound_track

# Demo of the sound section
if demo_sound is True:
    sound_track(None)
    exit()

# In[1]
# Get the frames of the video
video_var = list(video_to_frames(FRAME_F, VIDEO))
# Variables of the video and of the frames
video_length = video_var[0]
height = int(video_var[1])
width = int(video_var[2])

# In[2]
# Motion Capture
err, grid_size, frame_list = motion_capt(video_var)
if err is -1:  # Check for errors
    print(FAIL + "[Error] wrong execution of motion_capt in main" + ENDC)
    exit(-1)

# In[3]
# Replacement of the Background and of the Monkey
err = replace(BLUE)
if err is -1:  # Check for errors
    print(FAIL + "[Error] wrong execution of replace(1) in main" + ENDC)
    exit(-1)

# In[4]
# Draw the stickman
err = draw_stickman(frame_list, (BG_R_F + BG_R_N), BG_R_T, video_length, grid_size)
if err is -1:  # Check for errors
    print(FAIL + "[Error] wrong execution of draw_stickman in main" + ENDC)
    exit(-1)

# In[5]
# Replacement the rest of red of the frame
err = replace(BLACK)
if err is -1:  # Check for errors
    print(FAIL + "[Error] wrong execution of replace(2) in main" + ENDC)
    exit(-1)

# Create the video with the Monkey and the Background replaced
create_folder(BG_R_V_F)
create_video(width, height, video_length, BG_R_V_F + BG_R_V, [BG_R_F + BG_R_N, BG_R_T])

# In[6]
# Create the intelligent objects
err, frame_list = create_objects(frame_list, (BG_R_F + BG_R_N), BG_R_T, video_length)
if err is -1:  # Check for errors
    print(FAIL + "[Error] wrong execution of create_objects in main" + ENDC)
    exit(-1)

# Create the video with the Intelligent Objects
create_folder(INTE_V_F)
create_video(width, height, video_length, INTE_V_F + INTE_V, [INTE_F + INTE_N, INTE_T])

# In[7]
# Sound track
err = sound_track(frame_list)
if err is -1:  # Check for errors
    print(FAIL + "[Error] wrong execution of sound_track in main" + ENDC)
    exit(-1)
