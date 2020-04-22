import unittest
import constant
import functions
import cv2
import random


class TestGeneral(unittest.TestCase):

    def test_video_to_frames(self):
        """
        Check that when we convert a video to frames the height, width and the length are valid values
        """
        video_variables = list(
            functions.video_to_frames("../" + constant.FRAME_SAVE_PATH, "../" + constant.PATH_TO_VIDEO))
        self.assertGreater(video_variables[0], 0)
        self.assertGreater(video_variables[1], 0)
        self.assertGreater(video_variables[2], 0)

    def test_odd_grid(self):
        """
        Test that the size of the grid is odd
        """
        grid_size = functions.set_grid(576, 720, constant.MAX_GRID, constant.MIN_GRID)
        self.assertNotEqual(grid_size % 2, 0)

    def test_column_row_grid(self):
        """
        Test that the number of columns and rows after calculating the grid map is the
        expected one according to the original image size
        """
        img = cv2.imread(constant.TEST_FRAME_PATH)
        grid_size = 3
        height, width, channels = img.shape
        column = int(width / grid_size)
        row = int(height / grid_size)
        img_map, row, column = functions.grid_map(img, grid_size)
        self.assertEqual(height / grid_size, row)
        self.assertEqual(width / grid_size, column)

    def test_not_none_grid(self):
        """
        Test that the map grid obtained is not None
        """
        img = cv2.imread(constant.TEST_FRAME_PATH)
        grid_size = 3
        img_map, row, column = functions.grid_map(img, grid_size)
        self.assertNotEqual(img_map, None)

    def test_random_block(self):
        """
        Test that a random block is the same int he map as the one in the image
        """
        img = cv2.imread(constant.TEST_FRAME_PATH)
        grid_size = 3
        img_map, row, column = functions.grid_map(img, grid_size)
        random_x = random.randint(1, column)
        random_y = random.randint(1, row)
        x_origin = ((random_x + 1) * grid_size) - grid_size
        y_origin = ((random_y + 1) * grid_size) - grid_size
        for i in range(grid_size):
            for j in range(grid_size):
                self.assertEqual(img_map[random_y][random_x][j][i].all(), img[j + y_origin][i + x_origin].all())


class TestBorder(unittest.TestCase):

    def test_check_borders1(self):
        """
        Check the correct border calculation when
        the X and Y values goes out from the left
        Assuming max_len = 5:
        (0, 0) => X: {0, 5} Y: {0, 5}
        """
        x = 0
        y = 0
        border = functions.check_borders(x, y, 100, 100)
        self.assertEqual(0, border[0])
        self.assertEqual(5, border[1])
        self.assertEqual(0, border[2])
        self.assertEqual(5, border[3])

    def test_check_borders2(self):
        """
        Check the correct border calculation when
        the X values goes out from the left
        Assuming max_len = 5:
        (2, 20) => X: {0, 7} Y: {15, 25}
        """
        x = 2
        y = 20
        border = functions.check_borders(x, y, 100, 100)
        self.assertEqual(0, border[0])
        self.assertEqual(7, border[1])
        self.assertEqual(15, border[2])
        self.assertEqual(25, border[3])

    def test_check_borders3(self):
        """
        Check the correct border calculation when
        the X values goes out from the left
        Assuming max_len = 5:
        (0, 3) => X: {0, 8}  Y: {0, 5}
        """
        x = 3
        y = 0
        border = functions.check_borders(x, y, 100, 100)
        self.assertEqual(0, border[0])
        self.assertEqual(8, border[1])
        self.assertEqual(0, border[2])
        self.assertEqual(5, border[3])

    def test_check_borders4(self):
        """
        Check the correct border calculation when
        the X values goes out from the left and
        Y values goes out from the right
        Assuming max_len = 5:
        (98, 7) => X: {2, 12}  Y: {93, 99}
        """
        x = 7
        y = 98
        border = functions.check_borders(x, y, 100, 100)
        self.assertEqual(2, border[0])
        self.assertEqual(12, border[1])
        self.assertEqual(93, border[2])
        self.assertEqual(99, border[3])

    def test_check_borders5(self):
        """
        Check the correct border calculation when
        the X values goes out from the left
        Assuming max_len = 5:
        (97, 5) => X: {0, 11}  Y: {92, 99}
        """
        x = 5
        y = 97
        border = functions.check_borders(x, y, 100, 100)
        self.assertEqual(0, border[0])
        self.assertEqual(10, border[1])
        self.assertEqual(92, border[2])
        self.assertEqual(99, border[3])

    def test_check_borders6(self):
        """
        Check the correct border calculation when
        the X values goes out from the left
        Assuming max_len = 5:
        (99, 99) => X: {94, 99}  Y: {94, 99}
        """
        x = 99
        y = 99
        border = functions.check_borders(x, y, 100, 100)
        self.assertEqual(94, border[0])
        self.assertEqual(99, border[1])
        self.assertEqual(94, border[2])
        self.assertEqual(99, border[3])

    def test_check_borders7(self):
        """
        Check the correct border calculation when
        the map is lower than twice the grid size
        Assuming max_len = 5: and map_size = 3
        (1, 1) => X: {0, 2}  Y: {0, 2}
        """
        x = 1
        y = 1
        border = functions.check_borders(x, y, 3, 3)
        self.assertEqual(0, border[0])
        self.assertEqual(2, border[1])
        self.assertEqual(0, border[2])
        self.assertEqual(2, border[3])

    def test_check_borders_None1(self):
        """
        Wrong inputs values
        """
        x = -1
        y = 1
        border = functions.check_borders(x, y, 3, 3)
        self.assertEqual(-1, border[0])
        self.assertEqual(-1, border[1])
        self.assertEqual(0, border[2])
        self.assertEqual(2, border[3])

    def test_check_borders_None2(self):
        """
        Wrong inputs values
        """
        x = 4
        y = 1
        border = functions.check_borders(x, y, 3, 3)
        self.assertEqual(-1, border[0])
        self.assertEqual(-1, border[1])
        self.assertEqual(0, border[2])
        self.assertEqual(2, border[3])