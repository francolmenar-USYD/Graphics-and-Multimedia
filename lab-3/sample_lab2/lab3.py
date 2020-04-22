# In[1]

# IMPORT
from imageio import imread, imsave
import matplotlib
from matplotlib import pyplot as plt
import numpy as np

# matploit inline

# In[2]
# Read image
print('Raw Image')
raw_img = imread('coins2.jpg')
plt.figure(1)
plt.imshow(raw_img)
plt.show()


# In[3]
# Turn the input picture to greyscale
def to_grey_scale(img):
    (h, w, c) = img.shape
    processed_img = np.zeros((h, w))
    for row_idx in range(img.shape[0]):
        for col_idx in range(img.shape[1]):
            rgb_component = img[row_idx][col_idx]
            grey_value = rgb_component[0] * 0.212671 + 0.715160 * rgb_component[1] + 0.072169 * rgb_component[2]
            processed_img[row_idx][col_idx] = grey_value
    processed_img = np.uint8(processed_img)
    return processed_img


# In[4]
# Turn the input img to a grey img
greyImg = to_grey_scale(raw_img)
plt.figure(2)
plt.imshow(greyImg, cmap="gray")
plt.show()


# In[5]
# Turn the input image to a binary image
def to_binary(img):
    binImg = np.zeros(img.shape)
    for row_idx in range(img.shape[0]):
        for col_idx in range(img.shape[1]):
            actual_pixel = img[row_idx][col_idx]
            if actual_pixel < 128:
                binImg[row_idx][col_idx] = 0
            else:
                binImg[row_idx][col_idx] = 255
    binImg = np.uint8(binImg)
    return binImg


# In[6]
# Turn the image to a binary image
print(greyImg.shape)  # 2 Dimensions image
binImg = to_binary(greyImg)
plt.figure(3)
plt.imshow(binImg, cmap="gray")
plt.show()


# In[7]
# Perform a dilation to the given input image using the SE
def dilation(img, SE):
    return 1


# In[8]
# Call the dilation method
SE = np.array([[1, 1, 1],
                   [1, 1, 1],
                   [1, 1, 1]])
dilated_img = dilation(binImg, SE)
