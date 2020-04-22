import cv2
import numpy as np
import matplotlib.pyplot as plt


# function

def dilateErode2D(img_in, kernel, type):
    assert type == 'dilate' or type == 'erosion'
    img = img_in[:, :, 0]
    final = np.zeros(img_in.shape)
    newimg = np.copy(img)

    kernelSize = kernel.shape[0]
    radius = int(kernelSize / 2)

    h, w = img.shape
    for x in range(radius, h - radius):
        for y in range(radius, w - radius):
            demo_array = img[x - radius: x + radius + 1, y - radius: y + radius + 1]
            if type == 'dilate':
                result = np.amax(demo_array * kernel)
            else:
                result = np.amin(demo_array * kernel)
            newimg[x][y] = result

    final[:, :, 0] = newimg
    final[:, :, 1] = newimg
    final[:, :, 2] = newimg

    return final


img = cv2.imread('./sample_lab2/coin.png')
print(img.shape)
img_grey = img

# Turn the original image into grey scale one

img_new_grey = 0.212671 * img[:, :, 2] + 0.715160 * img[:, :, 0] + 0.072169 * img[:, :, 1]
img_grey[:, :, 0] = img_new_grey
img_grey[:, :, 1] = img_new_grey
img_grey[:, :, 2] = img_new_grey

# Binary Threshold

img_thres = ((img_grey > 127) + np.zeros(img_grey.shape)) * 255

cv2.imwrite('coin_pp.png', img_thres)

kernel = np.ones((3, 3), np.uint8)

# Get the images. ours: result from our code, cv2: result from the functions defined in opencv library.
# If there is nothing wrong, your result should be the same as the opencv's.

erosion_ours = dilateErode2D(img_in=img_thres, kernel=kernel, type='erosion')
plt.imshow(erosion_ours)
plt.show()

erosion_cv2 = cv2.erode(img_thres, kernel, iterations=1)

dilation_ours = dilateErode2D(img_in=img_thres, kernel=kernel, type='dilate')
plt.imshow(dilation_ours)
plt.show()

dilation_cv2 = cv2.dilate(img_thres, kernel, iterations=1)

openning_ours = dilateErode2D(erosion_ours, kernel, type='dilate')
plt.imshow(openning_ours)
plt.show()

opening_cv2 = cv2.morphologyEx(img_thres, cv2.MORPH_OPEN, kernel)
# opening_cv2_1 = cv2.dilate(erosion, kernel, iterations=1)   # An alternative way

closing_ours = dilateErode2D(dilation_ours, kernel, type='erosion')
plt.imshow(closing_ours)
plt.show()

closing_cv2 = cv2.morphologyEx(img_thres, cv2.MORPH_CLOSE, kernel)
# closing_cv2_1 = cv2.erode(dilation, kernel, iterations=1)   # An alternative way

cv2.imwrite('./demo_solution/ours_erosion.png', erosion_ours)
cv2.imwrite('./demo_solution/cv2_erosion.png', erosion_cv2)

cv2.imwrite('./demo_solution/ours_dilation.png', dilation_ours)
cv2.imwrite('./demo_solution/cv2_dilation.png', dilation_cv2)

cv2.imwrite('./demo_solution/ours_open.png', openning_ours)
cv2.imwrite('./demo_solution/cv2_open.png', opening_cv2)

cv2.imwrite('./demo_solution/ours_close.png', closing_ours)
cv2.imwrite('./demo_solution/cv2_close.png', closing_cv2)
