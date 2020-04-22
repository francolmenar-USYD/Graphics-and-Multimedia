# In[0]
import numpy as np
import cv2
import os
import sys


def createBG():
    """
    Reads a video and saves its frames to the Background folder
    """
    # Read the video
    cap = cv2.VideoCapture('../Quadrangle.mov')
    if not cap.isOpened():
        print('Quadrangle.mov not opened')
        sys.exit(1)
    # Characteristics of the video
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    bgctr = 1  # The total number of background frames
    count = 0
    while (1):
        ret, frame = cap.read()
        if not ret:
            break  # End of the video
        # Save the original frame into background
        cv2.imwrite('background/frame%d.tif' % count, frame)
        cv2.putText(img=frame, text='phase 1: %d%%' % int(100 * count / length), org=(int(0), int(frame.shape[1] / 2)),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.7,
                    color=(0, 255, 0))
        cv2.imshow('Background', frame)
        count += 1
        if cv2.waitKey(30) & 0xff == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    # In[1]
    changeBG(count, frame_width, frame_height)


def changeBG(count_a, frame_width, frame_height):
    """
    Change the background with the frames previously obtained
    """
    bgctr = count_a
    count = 0
    # Read the monkey video
    cap = cv2.VideoCapture('../monkey.avi')
    if not cap.isOpened():
        print('monkey.avi not opened')
        sys.exit(1)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    while (1):
        # Read frame
        ret, monkeyframe = cap.read()
        if not ret:
            break
        # Read the background frame
        bg = cv2.imread('background/frame%d.tif' % (count % bgctr))
        if bg is None:
            print('ooops! no bg found BG/frame%d.tif' % (count % bgctr))
            break
        # overwrite the background
        for x in range(monkeyframe.shape[0]):
            for y in range(monkeyframe.shape[1]):
                # If the pixel of the Monkey video is Blue we change it to the BG
                if monkeyframe[x][y][0] < BLUE:
                    bgx = int((x / monkeyframe.shape[0]) * bg.shape[0])
                    bgy = int((y / monkeyframe.shape[1]) * bg.shape[1])
                    for z in range(3):
                        bg[bgx][bgy][z] = monkeyframe[x][y][z]
        cv2.imwrite('composite/composite%d.tif' % count, bg)
        cv2.putText(img=bg, text='phase 2: %d%%' % int(100 * count / length), org=(int(0), int(bg.shape[1] / 2)),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.7,
                    color=(0, 255, 0))
        cv2.imshow('Monkey in Quadrangle', bg)

        count += 1
        if cv2.waitKey(30) & 0xff == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    createVideo(frame_width, frame_height, length)


def createVideo(frame_width, frame_height, length):
    count = 0
    out = cv2.VideoWriter('happy_monkey.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10,
                          (int(frame_width), int(frame_height)))
    while (1):
        img = cv2.imread('composite/composite%d.tif' % count)
        if img is None:
            break;
        print('phase 3: saving video %d%%' % int(100 * count / length))
        out.write(img)
        count += 1
    out.release()
    cv2.destroyAllWindows()

BLUE = 120

# Directories are coming
if not os.path.isdir(os.path.join(os.getcwd(), 'background')):
    os.mkdir("background")
else:
    print('background already exists')

if not os.path.isdir(os.path.join(os.getcwd(), 'composite')):
    os.mkdir("composite")
else:
    print('composite already exists')
createBG()
