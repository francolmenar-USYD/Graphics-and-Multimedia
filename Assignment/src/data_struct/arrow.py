import cv2
from src.constants.variables import *


def draw_head(img, arrowhead):
    """
    Draw the head of the stickman
    :param img: Image to draw in
    :param arrowhead: Coordinates of the arrowhead
    :return: The image with the head of the stickman
    """
    cv2.line(img, (arrowhead[0][0], arrowhead[0][1]),
             (arrowhead[1][0], arrowhead[1][1]),
             0, BODY_THICK)
    cv2.line(img, (arrowhead[1][0], arrowhead[1][1]),
             (arrowhead[2][0], arrowhead[2][1]),
             0, BODY_THICK)
    cv2.line(img, (arrowhead[2][0], arrowhead[2][1]),
             (arrowhead[0][0], arrowhead[0][1]),
             0, BODY_THICK)
    return img


def draw_stick(img, stick):
    """
    Draw the head of the stickman
    :param img: Image to draw in
    :param stick: Coordinates of the stick to draw
    :return: The image with the part of the stickman
    """
    cv2.line(img, (stick[0][0], stick[0][1]),
             (stick[1][0], stick[1][1]),
             0, BODY_THICK)
    return img


def draw_tail(img, tail):
    """
    Draw the head of the stickman
    :param img: Image to draw in
    :param tail: Coordinates of the tail to draw
    :return: The image with the part of the stickman
    """
    cv2.line(img, (tail[0][0][0], tail[0][0][1]),
             (tail[0][1][0], tail[0][1][1]),
             0, BODY_THICK)
    cv2.line(img, (tail[1][0][0], tail[1][0][1]),
             (tail[1][1][0], tail[1][1][1]),
             0, BODY_THICK)
    return img


class Arrow:

    def __init__(self, arrowhead, stick, tail):
        self.arrowhead = arrowhead
        self.stick = stick
        self.tail = tail

    def draw(self, img):
        """
        Draw the whole Stickman in the image
        :param img: Image to draw in
        :return: The image with the stickman
        """
        img = draw_head(img, self.arrowhead)
        img = draw_stick(img, self.stick)
        img = draw_tail(img, self.tail)
        return img

    def to_string(self):
        """
        Prints the coordinates of the StickMan
        """
        print("Coordinates of the Arrow:")
        print('\tArrow Head: [%s]' % ', '.join(map(str, self.arrowhead)))
        print('\tStick: [%s]' % ', '.join(map(str, self.stick)))
        print('\tTail: [%s]' % ', '.join(map(str, self.tail)))
