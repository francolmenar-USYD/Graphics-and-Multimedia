import cv2
from src.constants.variables import *


def draw_head(img, head, thick):
    """
    Draw the head of the stickman
    :param img: Image to draw in
    :param head: Coordinates of the head
    :return: The image with the head of the stickman
    """
    cv2.circle(img, (head[0], head[1]), thick, (0, 0, 0), -1)
    return img


def draw_part(img, part):
    """
    Draw the head of the stickman
    :param img: Image to draw in
    :param part: Coordinates of the part to draw
    :return: The image with the part of the stickman
    """
    cv2.line(img, (part[0][0], part[0][1]),
             (part[1][0], part[1][1]),
             0, BODY_THICK)
    return img


class StickMan:

    def __init__(self, head, body, r_arm, l_arm, r_leg, l_leg, rot_arm, rot_leg):
        self.head = head
        self.body = body
        self.r_arm = r_arm
        self.l_arm = l_arm
        self.r_leg = r_leg
        self.l_leg = l_leg
        self.rot_arm = rot_arm
        self.rot_leg = rot_leg

    def draw(self, img, thick):
        """
        Draw the whole Stickman in the image
        :param img: Image to draw in
        :return: The image with the stickman
        """
        img = draw_head(img, self.head, thick)
        img = draw_part(img, self.body)
        img = draw_part(img, self.r_arm)
        img = draw_part(img, self.l_arm)
        img = draw_part(img, self.r_leg)
        img = draw_part(img, self.l_leg)
        return img

    def to_string(self):
        """
        Prints the coordinates of the StickMan
        """
        print("Coordinates of the stickman:")
        print('\tHead: [%s]' % ', '.join(map(str, self.head)))
        print('\tBody: [%s]' % ', '.join(map(str, self.body)))
        print('\tRight Arm: [%s]' % ', '.join(map(str, self.r_arm)))
        print('\tLeft Arm: [%s]' % ', '.join(map(str, self.l_arm)))
        print('\tRight Leg: [%s]' % ', '.join(map(str, self.r_leg)))
        print('\tLeft Leg: [%s]' % ', '.join(map(str, self.l_leg)))
