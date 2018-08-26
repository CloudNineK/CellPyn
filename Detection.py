# from PIL import Image
import glob
import sys
import cv2
import numpy as np
import pandas as pd 
from matplotlib import pyplot as plt

def pipelineDraft(): 
    # create panda dataframe
    pd.DataFrame() 

def genThreshold(img):
    """ Return a thresholded version of img"""

    # Blur image to facilitate thresholding
    blur = cv2.medianBlur(img, 3)

    # Greyscale image for thresholding
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

    # Adaptive Threshold
    th1 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY, 61, 2)

    # Binary Threshold
    # ret, th2 = cv2.threshold(gray, 85, 255, cv2.THRESH_BINARY)

    return th1


def getFrames(vid):
    """ Returns an array of opencv image objects corresponding to each frame in
        the supplied video stream

        vid: supported opencv video format (e.g avi, mp4)
    """

    # Create opencv vidcap from filename
    vidcap = cv2.VideoCapture(vid)

    success = True
    frames = []

    # Append frames as opencv images to list
    while (success):
        success, image = vidcap.read()
        if success:
            frames.append(image)

    return frames


def genCircles(th, outImg):
    """ Returns a tuple containing a numpy array of circles and an image with
        the circles drawn on it
    """

    # Warning: may be long depending on the image
    circles = cv2.HoughCircles(th, cv2.HOUGH_GRADIENT, 1, 20, param1=100,
                               param2=10, minRadius=5, maxRadius=30)

    # convert the (x, y) coordinates and radius of the circles to integers
    circles = np.round(circles[0, :]).astype("int")

    # loop over the (x, y) coordinates and radius of the circles
    for (x, y, r) in circles:
        # draw the circle in the output image, then draw a rectangle
        # corresponding to the center of the circle
        # cv2.circle(outImg, (x, y), r, (0, 255, 0), 4)
        cv2.rectangle(outImg, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255),
                      -1)

    return (circles, outImg)


def removeColor(img):
    """
    """

    lower = np.array([0, 70, 0])
    upper = np.array([90, 255, 90])
    mask = cv2.inRange(img, lower, upper)
    out = cv2.bitwise_and(img, img, mask=mask)

    return out


def display(img):
    """ """

    plt.imshow(frames[0])
    plt.show()


def process(img):
    """ """

    # Remove all nongreen color from image
    green = removeColor(img)

    # Copy
    mask = np.zeros_like(img)

    # Threshold and detect circles
    th = genThreshold(green)
    th2 = cv2.cvtColor(th, cv2.COLOR_GRAY2RGB)
    circles, circ = genCircles(th, mask)

    return mask


def tracking(frames):
    """ Heavily based on OpenCV Tutorial for Lucas-Kanade Optical Flow
    """


    # params for ShiTomasi corner detection
    maxCorners = 2000  # This will need to be adjustable
    feature_params = dict(maxCorners=maxCorners,
                          qualityLevel=0.3,
                          minDistance=11,
                          blockSize=7)

    # Parameters for lucas kanade optical flow
    lk_params = dict(winSize=(15,15),
                     maxLevel=5,
                     criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    mask = np.zeros_like(frames[0])

    oldFrame = frames[0]

    # Take first frame and find corners in it
    p0 = cv2.goodFeaturesToTrack(oldFrame, mask = None, **feature_params)

    # Create some random colors
    color = (100,100,255)

    images = []
    for k in range(1, len(frames)):

        newFrame = frames[k]

        # Calculate Optical Flow
        p1, st, error = cv2.calcOpticalFlowPyrLK(oldFrame, newFrame, p0, None, **lk_params)

        # Select good points
        good_new = p1[st == 1]
        good_old = p0[st == 1]

        # draw the tracks
        for i,(new,old) in enumerate(zip(good_new,good_old)):
            a,b = new.ravel()
            c,d = old.ravel()
            mask = cv2.line(mask, (a, b), (c, d), color, 4)
            newFrame = cv2.circle(newFrame, (a, b), 5, color, -1)

        img = cv2.add(newFrame, mask)
        images.append(img.copy())

        oldFrame = newFrame.copy()
        p0 = good_new.reshape(-1,1,2)

    return images


def load_images(folder):
    images = []
    for img in glob.glob(folder + "/*.jpg"):
        i = cv2.imread(img)
        images.append(i)

    return images


def outFrames(frames, fold):
    for k in range(len(frames)):
        cv2.imwrite(fold + "/out{}.jpg".format(k), frames[k])

if __name__ == "__main__":

    # Get list of frames
    frames = getFrames(sys.argv[1])

    # Threshold circles
    # thCircles = load_images('th')
    # Raw circles
    # rawCircles = load_images('out')

    i = 0
    circleFrames = []
    for frame in frames:
        print("Processing frame {}...".format(i))
        out = process(frame)
        out = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
        circleFrames.append(out)
        i += 1

    masks = tracking(circleFrames)


    # outFrames(thCircles, 'thC')
    # outFrames(rawCircles, 'rC')
    outFrames(masks, 'tk')

    print("exit")
