from src.data_struct.arrow import Arrow
from src.data_struct.stickman import StickMan
from src.functions.func import *

# Boolean representing if the Arrow is hitting the Stickman
intersect = False
# If a new Arrow has to be drawn
new_arrow = True
arrow_count = 0
# Speed of the arrow
speed = 30


def create_objects(frame_list, str_pre, str_aft, video_length):
    """
    Create the Intelligent Objects and save the frames in the correct folder
    :param frame_list:
    :param str_pre:
    :param str_aft:
    :param video_length:
    :return: 0 if there is no problem and the frame_list with the Arrow and mini Stickman objects added
    """
    # Folder for the background replaced frames
    create_folder(INTE_F)
    i = 0
    # If we are testing we do not use all the frames
    if not test:
        length = video_length - 2
    # The whole video
    else:
        length = test_val
    dirname = os.path.dirname(__file__)
    while i < length:
        # Read frame
        img = cv2.imread(dirname + '/' + str_pre + "%d" % i + str_aft)
        # Create the arrow
        global new_arrow
        arrow = create_arrow(i, frame_list)
        # Add the arrow to the  Frame Data
        frame_list[i].arrow = arrow
        # Create the stickman
        mini_stickman = create_stickman(i, frame_list)
        # Add the mini stickman to the Frame Data
        frame_list[i].mini_stickman = mini_stickman
        global intersect
        # If the Arrow is not hitting the Stickman the arrow and the Stickman are drawn
        if not intersect:
            img = frame_list[i].arrow.draw(img)
            img = frame_list[i].mini_stickman.draw(img, 6)
        # If the Arrow is hitting the Stickman the Arrow is not displayed
        else:
            # The Arrow is not hitting the Stickman any more
            intersect = False
            # The Arrow is going to be displayed in the origin position the next iteration
            new_arrow = True
            # Draw the mini Stickman with a smaller head
            img = frame_list[i].mini_stickman.draw(img, 4)
        # Save the frame with the objects
        cv2.imwrite(dirname + '/' + INTE_F + INTE_N + "%d" % i + INTE_T, img)
        # Check if the Arrow is hitting the Stickman
        check_collision(frame_list[i])
        i += 1
    return 0, frame_list


def create_arrow(index, frame_list):
    """
    Create the arrow which will be added to the image
    :param index: The index of the actual frame
    :param frame_list: List with the FrameData objects
    :return: The Arrow object
    """
    global new_arrow
    # Check if we have to draw the Arrow from the starting point
    if index is 0 or new_arrow:
        # Draw the Arrow in the starting point
        start_point = [130, 160]
        # The Arrow is relative to the starting point chosen
        arrow_head = [start_point, [start_point[0] - 5, start_point[1] + 5],
                      [start_point[0] - 5, start_point[1] - 5]]
        stick = [[start_point[0] - 5, start_point[1]], [start_point[0] - 15, start_point[1]]]
        tail = [[[start_point[0] - 15, start_point[1]], [start_point[0] - 20, start_point[1] - 5]],
                [[start_point[0] - 15, start_point[1]], [start_point[0] - 20, start_point[1] + 5]]]
        # The arrow does not have to be displayed in the original position the next iteration
        new_arrow = False
    # Move the arrow to the right
    else:
        # Get the previous Arrow
        old_arrow = frame_list[index - 1].arrow
        arrow_head = old_arrow.arrowhead
        # Update the position of the new Arrow using the speed
        for i in range(3):
            arrow_head[i][0] += speed

        stick = old_arrow.stick
        for i in range(2):
            stick[i][0] += speed

        tail = old_arrow.tail
        for i in range(2):
            for j in range(2):
                tail[i][j][0] += speed

    return Arrow(arrow_head, stick, tail)


def create_stickman(index, frame_list):
    """
    Creates the mini-stickman. If it is the first iteration it is drawn in a default position.
    If not, is drawn using the rotation of the arms of the big stickman of the previous frame
    :param index: Number of the actual frame
    :param frame_list: List with the FrameData objects
    :return: The Stickman object
    """
    # Check if we have to draw the Stickman for the first time
    if index is 0 or 1:
        # Create the smaller Stick Man in the default position
        rot_arm = [17, 4]
        rot_leg = [[10, -5], [-25, 0]]

        head = [60, 60]
        body = [head, [head[0], head[1] + 30]]

        r_arm = [[head[0], head[1] + 7],
                 [head[0] - 25, head[1] + 7]]
        l_arm = [[head[0], head[1] + 7],
                 [head[0] + 25, head[1] + 7]]

        r_leg = [[body[1][0], body[1][1]],
                 [body[1][0] + 5, body[1][1] + 20]]
        l_leg = [[body[1][0], body[1][1]],
                 [body[1][0] - 5, body[1][1] + 10]]

        # This part does not work properly and the Mini Stickman does not move
        r_arm[1][1] += rot_arm[0]
        l_arm[1][1] += rot_arm[1]

        r_leg[1][0] += rot_leg[0][0]
        r_leg[1][1] += rot_leg[0][1]

        l_leg[1][0] += rot_leg[1][0]
        l_leg[1][1] += rot_leg[1][1]
    # Draw the stickman using the rotation of the previous frame
    else:
        # Get the previous Stickman and Mini Stickman in order to calculate the new
        # position of the Mini Stickman in relation to them
        old_stickman = frame_list[index].stickman
        old_mini_stickman = frame_list[0].mini_stickman

        head = old_mini_stickman.head
        body = old_mini_stickman.body

        rot_arm = old_stickman.rot_arm
        rot_leg = old_stickman.rot_leg

        r_arm = old_mini_stickman.r_arm
        l_arm = old_mini_stickman.l_arm

        r_leg = old_mini_stickman.r_leg
        l_leg = old_mini_stickman.l_leg

        # This part does not work properly and the Mini Stickman does not move
        r_arm[1][1] += rot_arm[0]
        l_arm[1][1] += rot_arm[1]

        r_leg[1][0] += rot_leg[0][0]
        r_leg[1][1] += rot_leg[0][1]

        l_leg[1][0] += rot_leg[1][0]
        l_leg[1][1] += rot_leg[1][1]

    return StickMan(head, body, r_arm, l_arm, r_leg, l_leg, rot_arm, rot_leg)


def check_collision(frame):
    """
    Checks if the Arrow is hitting the body of the Stickman
    :param frame:
    :return: True if there is a collision and False otherwise
    """
    global intersect
    # Get the Arrow
    arrow = frame.arrow
    # Get the coordinates of the Stick Line of the Arrow
    arrow_y = arrow.arrowhead[0][1]
    arrow_point = arrow.arrowhead[0][0]
    # Check if there is an intersection between the Arrow Line and the Body
    intersect = check_intersection([[arrow_point, arrow_y], [arrow_point, arrow_y]], frame.stickman.body)
    return intersect


def check_intersection(line1, line2):
    """
    It checks if the two Lines intersect between them
    :param line1:
    :param line2:
    :return: True if they intersect and False otherwise
    """
    # The Mathematical Equation is applied
    X1 = line1[0][0]
    X2 = line1[1][0]
    X3 = line2[0][0]
    X4 = line2[1][0]

    Y1 = line1[0][1]
    Y2 = line1[1][1]
    Y3 = line2[0][1]
    Y4 = line2[1][1]

    I1 = [min(X1, X2), max(X1, X2)]
    I2 = [min(X3, X4), max(X3, X4)]

    Ia = [max(min(X1, X2), min(X3, X4)),
          min(max(X1, X2), max(X3, X4))]

    if max(X1, X2) < min(X3, X4):
        return False

    if ((Y1 - Y2) is 0) and ((X1 - X2) is 0):
        return True
    A1 = (Y1 - Y2) / (X1 - X2)
    if ((Y3 - Y4) is 0) and ((X3 - X4) is 0):
        return True
    A2 = (Y3 - Y4) / (X3 - X4)
    b1 = Y1 - A1 * X1
    b2 = Y3 - A2 * X3

    if A1 == A2:
        return False

    if ((b2 - b1) is not 0) and ((A1 - A2) is not 0):
        Xa = (b2 - b1) / (A1 - A2)

    if ((Xa < max(min(X1, X2), min(X3, X4))) or
            (Xa > min(max(X1, X2), max(X3, X4)))):
        return False
    else:
        return True
