from src.data_struct.stickman import StickMan
from src.functions.func import *


def replace(color):
    """
    Creates the folder to store the frames with the background replaced
    :param color: The color that we want to replaced
    :return: 0 if there is no problem. Otherwise -1 is returned
    """
    # Get the frames of the video
    video_var = list(video_to_frames(BG_F, BG))
    video_length = video_var[0]
    # Folder for the background replaced frames
    create_folder(BG_R_F)

    dirname = os.path.dirname(__file__)
    # Paths to the motion frames and to the background
    if color is BLUE:
        origin_str = [(dirname + "/" + MOTION_F + MOTION_N), MOTION_T]
    else:
        origin_str = [(dirname + "/" + BG_R_F + BG_R_N), BG_R_T]
    bg_str = [(dirname + "/" + BG_F + BG_N), BG_T]
    out_str = [(dirname + "/" + BG_R_F + BG_R_N), BG_R_T]
    # Replace the Red pixels of the Monkey background
    err = replace_bg(video_length, color, origin_str, bg_str, out_str)
    if err is -1:  # Check for errors
        print(FAIL + "[Error] wrong replacement of the background in create_folder, replace" + ENDC)
        exit(-1)
    return 0


def replace_bg(video_length, color, origin_str, bg_str, out_str):
    """
    Replace the color of the video
    :param video_length: Length of the video
    :param color: The color that we want to replaced
    :param origin_str: Path to the frames of the original video
    :param bg_str: Path to the frames of the background video
    :param out_str: Path to the folder containing the output frames
    :return: 0 if there is no problem. Otherwise -1 is returned
    """
    i = 0
    start_progress("Replacing the background")
    if not test:
        length = video_length - 2
    else:
        length = test_val
    # while 1:
    while i <= length:
        progress((i / length) * 100)
        # Read Original Frame
        origin = cv2.imread(origin_str[0] + '%d' % i + origin_str[1])
        if origin is None:  # Check for errors
            break
        # Read the background frame
        bg = cv2.imread(bg_str[0] + "%d" % i + bg_str[1])
        if bg is None:
            print(FAIL + "[Error] No  bg frame found in replace()" + ENDC)
            return -1
        # overwrite the background
        overwrite(origin, bg, i, color, out_str)
        i += 1
    end_progress()
    return 0


def overwrite(origin, new_comp, f_id, color, out_str):
    """
    It overwrites a given color from the origin frame with the new frame
    :param origin: Frame which is going to have removed the color
    :param new_comp: Frame which is going to be inserted into origin
    :param f_id: Frame id for writing it
    :param color: Color to be overwrite
    :param out_str: Path to the folder containing the output frames
    """
    for x in range(origin.shape[0]):
        for y in range(origin.shape[1]):
            # If the pixel of the Origin video is the chosen color we change it to the New_comp
            if color == BLUE:
                if origin[x][y][0] < BLUE:
                    new_x = int((x / origin.shape[0]) * new_comp.shape[0])
                    new_y = int((y / origin.shape[1]) * new_comp.shape[1])
                    for z in range(3):
                        new_comp[new_x][new_y][z] = origin[x][y][z]
            if color == BLACK:
                # If the pixel of the Origin video is the chosen color we change it to the New_comp
                if (int(origin[x][y][0]) is 0) & (int(origin[x][y][1]) is 0) & (int(origin[x][y][2]) is 0):
                    for z in range(3):
                        new_comp[x][y][z] = origin[x][y][z]
    cv2.imwrite(out_str[0] + "%d" % f_id + out_str[1], new_comp)


def draw_stickman(frame_list, str_pre, str_aft, video_length, grid_size):
    i = 0
    if not test:
        length = video_length - 2
    else:
        length = test_val
    dirname = os.path.dirname(__file__)
    start_progress("Drawing the stickman")
    while i < length:
        progress((i / length) * 100)
        # Read image
        img = cv2.imread(dirname + "/" + str_pre + "%d" % i + str_aft)
        # Calculate the center of the components of the stickman
        center = get_center(img)
        # Head
        head = get_head(center)
        # Body
        body = get_body(head)

        # Get the rotation of the monkey
        if i is 0:  # Initial position of the monkey
            rot_arm = [17, 4]
            rot_leg = [[10, -5], [-25, 0]]
            old_rot = [[0, 0],
                       [[0, 0], [0, 0]]]
        else:  # Get the rotation using the displacement
            old_stickman = frame_list[i - 1].stickman
            rot_arm, rot_leg = get_rotation(frame_list[i].disp, grid_size, body, old_stickman)
            old_rot = [old_stickman.rot_arm, old_stickman.rot_leg]

        # Right arm
        r_arm = get_r_arm(head, rot_arm[0], old_rot[0][0])
        # Left arm
        l_arm = get_l_arm(head, rot_arm[1], old_rot[0][1])
        # Right leg
        r_leg = get_r_leg(body, rot_leg[0])
        # Left leg
        l_leg = get_l_leg(body, rot_leg[1])
        # Create the stickman
        stickman = StickMan(head, body, r_arm, l_arm, r_leg, l_leg, rot_arm, rot_leg)
        # Save the stickman to the current frame
        frame_list[i].stickman = stickman
        # Draw the stickman in the correct position
        img = stickman.draw(img, HEAD_THICK)
        # Write the image with the stickman
        cv2.imwrite((dirname + "/" + BG_R_F + BG_R_N) + "%d" % i + BG_R_T, img)
        i += 1
    end_progress()
    return 0


def get_rotation(disp, grid_size, body, stickman):
    leg_rot = [[0, 0], [0, 0]]  # Default values
    arm_rot = [0, 0]
    for y_axis in range(len(disp) - 1):
        for x_axis in range(len(disp[0]) - 1):
            # Calculate the
            x_dest = disp[y_axis][x_axis][0] * grid_size
            x_origin = disp[y_axis][x_axis][1] * grid_size
            y_dest = disp[y_axis][x_axis][2] * grid_size
            y_origin = disp[y_axis][x_axis][3] * grid_size
            if x_dest != x_origin or y_dest != y_origin:
                # Right part of the body
                if x_dest > body[0][0]:
                    # Right Arm
                    if y_dest < body[1][1]:
                        arm_rot[0] = get_rot_r_arm(y_dest, y_origin, arm_rot, stickman)
                    # Right Leg
                    if y_dest > body[1][1]:
                        aux = [x_dest - x_origin, y_dest - y_origin]
                        if (abs(aux[0]) > abs(leg_rot[0][0])) & (abs(aux[1]) > abs(leg_rot[0][1])):
                            leg_rot[0] = [int(aux[0] / 2), int(aux[1] / 2)]
                # Left part of the body
                elif x_dest < body[0][0]:
                    # Left Arm
                    if x_dest < body[1][0]:
                        aux = y_dest - y_origin
                        if abs(aux) > abs(arm_rot[1]):
                            if stickman.l_arm[1][1] < y_dest:
                                aux = aux * (-1)
                            arm_rot[1] = aux * 2
                    # Left Leg
                    if y_dest > body[1][1]:
                        aux = [x_dest - x_origin, y_dest - y_origin]
                        if (abs(aux[0]) > abs(leg_rot[1][0])) & (abs(aux[1]) > abs(leg_rot[1][1])):
                            leg_rot[1] = [int(aux[0] / 2), int(aux[1] / 2)]
    return arm_rot, leg_rot


def get_rot_r_arm(y_dest, y_origin, arm_rot, stickman):
    aux = y_dest - y_origin
    if abs(aux) > abs(arm_rot[0]):
        if stickman.r_arm[1][1] > y_dest:
            aux = aux * (-1)
        arm_rot[0] = aux * 2
    return arm_rot[0]


def get_center(img):
    """
    Calculate the center of the stickman
    :param img: Frame to be used
    :return: the position of the center of the stickman, (X, Y)
    """
    center = np.array(find_center(to_binary(rgb2gray(img), 127, 255), 127))
    center[0] += OFF_CENTER_BG[0]
    center[1] += OFF_CENTER_BG[1]
    return center


def get_head(center):
    """
    Calculate the position of head
    :param center: Center of the stickman
    :return: the position of the head of the stickman, (X, Y)
    """
    return [center[0] + OFF_HEAD[0], center[1] + OFF_HEAD[1]]


def get_body(head):
    """
    Calculate the position of Body
    :param head: Head of the stickman
    :return: the position of the body of the stickman, ((X1, X2), (Y1, Y2))
    """
    body_rotation = 0
    body_start = head
    body_end = [0, 0]
    body_end[0] = head[0] + body_rotation
    body_end[1] = head[1] + OFF_BODY_Y
    return [body_start, body_end]


def get_r_arm(head, rot, old_rot):
    """
    Calculate the position of Right Arm
    :param rotation: Rotation of the arm
    :param head: Head of the stickman
    :return: the position of the arm of the stickman, ((X1, X2), (Y1, Y2))
    """
    r_arm_start = [0, 0]
    r_arm_start[0] = head[0]
    r_arm_start[1] = head[1] + OFF_A_ORIG
    r_arm_end = [0, 0]
    r_arm_end[0] = head[0] + OFF_RH_END[0]
    r_arm_end[1] = head[1] + OFF_RH_END[1] + int(rot/2) + old_rot
    return [r_arm_start, r_arm_end]


def get_l_arm(head, rot, old_rot):
    """
    Calculate the position of Left Arm
    :param head: Head of the stickman
    :return: the position of the arm of the stickman, ((X1, X2), (Y1, Y2))
    """
    l_arm_start = [0, 0]
    l_arm_start[0] = head[0]
    l_arm_start[1] = head[1] + OFF_A_ORIG
    l_arm_end = [0, 0]
    l_arm_end[0] = head[0] + OFF_LH_END[0]
    l_arm_end[1] = head[1] + OFF_LH_END[1] + rot + old_rot
    return [l_arm_start, l_arm_end]


def get_r_leg(body, rotation):
    """
    Calculate the position of Right Leg
    :param rotation: Rotation of the arm
    :param body: Body of the stickman
    :return: the position of the leg of the stickman, ((X1, X2), (Y1, Y2))
    """
    r_leg_start = [0, 0]
    r_leg_start[0] = body[1][0]
    r_leg_start[1] = body[1][1]
    r_leg_end = [0, 0]
    r_leg_end[0] = body[1][0] + OFF_RL_END[0] + rotation[0]
    r_leg_end[1] = body[1][1] + OFF_RL_END[1] + rotation[1]
    return [r_leg_start, r_leg_end]


def get_l_leg(body, rotation):
    """
    Calculate the position of Left Leg
    :param rotation: Rotation of the arm
    :param body: Body of the stickman
    :return: the position of the leg of the stickman, ((X1, X2), (Y1, Y2))
    """
    l_leg_start = [0, 0]
    l_leg_start[0] = body[1][0]
    l_leg_start[1] = body[1][1]
    l_leg_end = [0, 0]
    l_leg_end[0] = body[1][0] + OFF_LL_END[0] + rotation[0]
    l_leg_end[1] = body[1][1] + OFF_LL_END[1] + rotation[1]
    return [l_leg_start, l_leg_end]
