import cv2
import matplotlib.pyplot as plt
import os
import errno
import sys


def img_show(img, counter, mode, RGB):
    """
    Displays the given image
    :param RGB: Boolean representing if the input image is a RGB image or not
    :param mode: Cmap to display the image
    :param img: Image to display
    :param counter: The number of the figure
    :return: The updated counter of displayed images
    """
    plt.figure(counter)
    plt.axis('off')
    if not RGB:
        img_aux = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img_aux
    if mode is None:
        plt.imshow(img)
    else:
        plt.imshow(img, cmap=mode)
    plt.show()
    return counter + 1


def create_folder(name):
    """
    If a folder does not exist, it is created
    :param name: Name of the folder
    :return: 0 if there is no error. Otherwise -1 is returned
    """
    try:
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, name)
        os.makedirs(filename)
        return 0
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        return -1


def start_progress(title):
    """
    Display the Start of the execution of the process
    :param title: Name of the process
    :return: 0 if there is no error. Otherwise -1 is returned
    """
    global progress_x
    sys.stdout.write(title + ": [" + "-" * 40 + "]" + chr(8) * 41)
    sys.stdout.flush()
    progress_x = 0
    return 0


def progress(x):
    """
    Display the progress of the execution of the process
    :param x: Progress of the program
    :return: 0 if there is no error. Otherwise -1 is returned
    """
    global progress_x
    x = int(x * 40 // 100)
    sys.stdout.write("#" * (x - progress_x))
    sys.stdout.flush()
    progress_x = x
    return 0


def end_progress():
    """
    Print the end of the current process
    :return: 0 if there is no error. Otherwise -1 is returned
    """
    sys.stdout.write("#" * (40 - progress_x) + "]\n")
    sys.stdout.flush()
    return 0


def create_video(frame_width, frame_height, length, out_path, input_path):
    count = 0
    dirname = os.path.dirname(__file__)
    out_path = os.path.join(dirname, out_path)
    input_path[0] = os.path.join(dirname, input_path[0])
    out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 5,
                          (int(frame_width), int(frame_height)))
    start_progress("Creating video")
    while 1:
        progress((count / length) * 100)
        img = cv2.imread(input_path[0] + str(count) + input_path[1])
        if img is None:
            break
        out.write(img)
        count += 1
    end_progress()
    out.release()
    cv2.destroyAllWindows()
