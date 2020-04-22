import numpy as np
import cv2
import os


# Find the object coordinate by averaging the foreground coordinates
def findObj(frame, threshold):
    xsum = 0
    ysum = 0
    ctr = 0

    for x in range(frame.shape[0]):
        for y in range(frame.shape[1]):
            if frame[x][y][2] > threshold:
                xsum += x
                ysum += y
                ctr += 1
    xmean = 0
    ymean = 0

    if ctr <= 20:
        xmean = -1
        ymean = -1
    else:
        xmean = xsum / ctr
        ymean = ysum / ctr

    return (xmean, ymean)


# Draw a circle on the image
def drawbox(frame, centerx, centery, radius, color):
    for y in range(centerx - radius, centerx + radius):
        for x in range(centery - radius, centery + radius):
            cx = 0 if x < 0 else frame.shape[0]-1 if x > frame.shape[0] - 1 else x
            cy = 0 if y < 0 else frame.shape[1]-1 if y > frame.shape[1] - 1 else y
            for i in range(3):
                frame[cx][cy][i] = color[i]
    return frame


def create_folder():
    if not os.path.isdir(os.path.join(os.getcwd(), 'frames')):
        os.mkdir("frames")
    else:
        print('frames already exists')

    if not os.path.isdir(os.path.join(os.getcwd(), 'composite')):
        os.mkdir("composite")
    else:
        print('composite already exists')


create_folder()
# Kalman Filter para
dt = 1.0
accNoiseMag = 0.1
mNoiseX = 1
mNoiseY = 1
u = 0.005 # Define the acceleration magnitude
qEstimate = np.array([[0], [0], [0], [0]]) # Initized state--it has four components: [positionX; positionY; velocityX; velocityY] of the hexbug

Ez = np.array([[mNoiseX, 0.0],[0.0, mNoiseY]]) # Noise covariance
Ex = np.array([[pow(dt, 4.0)/4.0, 0.0, pow(dt, 3.0)/2.0, 0.0],
               [0.0, pow(dt, 4.0)/4.0, 0.0, pow(dt, 3.0)/2.0],
               [pow(dt, 3.0)/2.0, 0.0, pow(dt, 2.0), 0.0],
               [0.0, pow(dt, 3.0)/2.0, 0.0, pow(dt, 2.0)]])
P = np.copy(Ex)

# Define update equations in 2-D! (Coefficent matrices): A physics based model for where we expect the object to be [state transition (state + velocity)] + [input control (acceleration)]
A = np.array([[1, 0, dt, 0], [0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0, 1]]) # State update matrice
B = np.array([[pow(dt, 2)/2], [pow(dt, 2)/2], [dt], [dt]])
C = np.array([[1, 0, 0, 0], [0, 1, 0, 0]]) # This is our measurement function C, that we apply to the state estimate Q to get our expect next/new measurement
eye4 = np.eye(4) # 4X4 Identity matrix
cMeasure = np.array([[0], [0]]) # The object coordinates obtained from brightness segmentation

foreground = 250 # Foreground Threshold for Segmentation
# Store the coordinates found by intensity thresholding
coordListX = list()
coordListY = list()

# Store the coordinates found by kalman filter
coordListKX = list()
coordListKY = list()

framenumber = 0
framectr = 0
omovie = cv2.VideoCapture('/Users/fran/Documents/UC3M/Graph/lab5/pingpang.mov')

while(1):
    ret, frame = omovie.read()
    if not ret:
        break
    print('Extracting: %d' % framenumber)
    cv2.imwrite('frames/%d.tif' % framenumber, frame)
    framenumber += 1
omovie.release()
framectr = framenumber - 1
framenumber = 0

# Load the saved frames sequentially
height = None
width = None

while framenumber <= framectr:
    oframe = cv2.imread('frames/%d.tif' % framenumber)

    # Change frame to grey scale
    gframe = oframe.copy() # Grey scaled frame

    for y in range(gframe.shape[1]):
        for x in range(gframe.shape[0]):
            # Convert to gray scale
            g = 0.212671 * gframe[x][y][2] + 0.715160 * gframe[x][y][1] + 0.072169 * gframe[x][y][0]

            # Convert to binary
            for i in range(3):
                if g > foreground:
                    gframe[x][y][i] = 255
                else:
                    gframe[x][y][i] = 0

    # Get the initial state (object coordinates) from binary segmentation
    coord = findObj(gframe, 128) # coord is the centre of mass
                                 # coord[0] : y column
                                 # coord[1] : x row
    # *** Start kalman filter
    cMeasure[0][0] = coord[1]
    cMeasure[1][0] = coord[0]
    qEstimate = (np.matmul(A, qEstimate)) + (B*u)

    # Predict next covariance
    P = np.matmul(np.matmul(A, P), A.T) + Ex

    # Predicted measurement covariance
    # Kalman Gain
    tmp = np.matmul(np.matmul(C, P), C.T)+Ez
    if tmp.shape[0] == tmp.shape[1]:
        inversedM = np.linalg.inv(tmp)
    else:
        inversedM = np.linalg.pinv(tmp)
    K = np.matmul(np.matmul(P, C.T), inversedM)

    # Update the state estimate only when a valid segmentation tracking is available
    if cMeasure[0][0] > 0 and cMeasure[1][0] > 0:
        qEstimate = qEstimate + np.matmul(K, (cMeasure - (np.matmul(C, qEstimate))))

    # Update covariance estimation
    P = np.matmul((eye4 - np.matmul(K, C)), P)

    # Draw the tracked coordinate boxes on both frames
    oframe = drawbox(oframe, int(cMeasure[0][0]), int(cMeasure[1][0]), 5, (0, 0, 255))
    oframe = drawbox(oframe, int(qEstimate[0][0]), int(qEstimate[1][0]),5, (255 , 0, 0))
    gframe = drawbox(gframe, int(cMeasure[0][0]), int(cMeasure[1][0]), 5, (0, 0, 255))
    gframe = drawbox(gframe, int(qEstimate[0][0]), int(qEstimate[1][0]), 5, (255, 0, 0))
    print('frame %d/%d...\tx: %f\ty: %f\tkx: %f\tky: %f' % (framenumber, framectr,
          cMeasure[0][0],
          cMeasure[1][0],
          qEstimate[0][0],
          qEstimate[1][0]))
    oframe = cv2.resize(oframe, (0, 0), fx=0.5, fy=0.5)
    gframe = cv2.resize(gframe, (0, 0), fx=0.5, fy=0.5)

    # combine oframe and gframe and display it with a text
    combined_img = np.hstack((oframe, gframe))
    if height is None:
        height = int(combined_img.shape[0])
    if width is None:
        width = int(combined_img.shape[1])
    cv2.putText(img=combined_img, text='Processing Frame: %d/%d ...' % (framenumber, framectr), org=(10, 30),
                fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.7,
                color=(0, 255, 0))
    if cMeasure[0][0] < 0 or cMeasure[1][0] < 0:
        print('Object missing by intensity thresholding')
        cv2.putText(img=combined_img, text='Object missing by intensity thresholding', org=(10, 70),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.7,
                    color=(0, 255, 0))
    else:
        print('Object found by intensity thresholding')
        cv2.putText(img=combined_img, text='Object found by intensity thresholding', org=(10, 70),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.7,
                    color=(0, 255, 0))
        coordListX.append(coord[1])
        coordListY.append(coord[0])

    coordListKX.append(qEstimate[0][0])
    coordListKY.append(qEstimate[1][0])

    # Draw segments to show the tracks
    for i in range(len(coordListX)-2):
        cv2.line(combined_img, (int(coordListX[i]/2), int(coordListY[i]/2)), (int(coordListX[i+1]/2), int(coordListY[i+1]/2)), (0, 0, 255), 2)

    for i in range(len(coordListKX) - 2):
        cv2.line(combined_img, (int(coordListKX[i] / 2), int(coordListKY[i] / 2)), (int(coordListKX[i + 1] / 2), int(coordListKY[i + 1] / 2)),
                 (255, 0, 0), 2)
    cv2.imwrite('composite/composite%d.tif' % framenumber, combined_img)
    if cv2.waitKey(30) & 0xff == ord('q'):
        break
    framenumber += 1



count = 0
out = cv2.VideoWriter('happy_ping_pang.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (width, height))
while(1):
    img = cv2.imread('composite/composite%d.tif' % count)
    if img is None:
        break;
    print('phase 3: saving video %d%%' % int(100*count/framectr))
    out.write(img)
    count += 1
out.release()
cv2.destroyAllWindows()