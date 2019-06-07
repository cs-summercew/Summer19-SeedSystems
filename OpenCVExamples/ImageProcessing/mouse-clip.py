import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os
import os.path
import shutil

# NOTE: The code used in this file is heavily based off of the tutorial code in the following link, and contains more detail:
#       https://www.pyimagesearch.com/2015/03/09/capturing-mouse-click-events-with-python-and-opencv/
#       Some of the comment suggestions in the link were used too!

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
sel_rect_endpoint = []
cropping = False

def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
    global refPt, cropping, sel_rect_endpoint
 
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
    if event == cv.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True
 
	# check to see if the left mouse button was released
    elif event == cv.EVENT_LBUTTONUP:
	    # record the ending (x, y) coordinates and indicate that
	    # the cropping operation is finished
        refPt.append((x, y))
        cropping = False
 
		# draw a rectangle around the region of interest
        cv.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        cv.imshow(FILE_NAME, image)
    elif event == cv.EVENT_MOUSEMOVE and cropping:
        sel_rect_endpoint = [(x, y)]
    

original_dir = os.getcwd()
path = os.path.join(original_dir, "Bananna")
os.chdir(path)

FILE_NAME = "frame448.png"
image = cv.imread(FILE_NAME)
clone = image.copy()
cv.namedWindow(FILE_NAME)
cv.setMouseCallback(FILE_NAME, click_and_crop)
while True:
    # display the image and wait for a keypress
    if not cropping:
        cv.imshow(FILE_NAME, image)
    elif cropping and sel_rect_endpoint:
        rect_cpy = image.copy()
        cv.rectangle(rect_cpy,refPt[0],sel_rect_endpoint[0],(0,255,0), 1)
        cv.imshow(FILE_NAME, rect_cpy)
    key = cv.waitKey(1) & 0xFF
    # if the 'r' key is pressed, reset the cropping region
    if key == ord("r"):
        image = clone.copy()
        print("You reset the image!")
    # if the esc key is pressed, break from the loop
    elif key == 27:
        cv.destroyWindow(FILE_NAME)
        print("You chose your clipping!")
        break

# if there are two reference points, then crop the region of interest
# from the image and display it
if len(refPt) == 2:
    clip = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    while True:
        cv.imshow("Clipping", clip)
        key = cv.waitKey(1) & 0xFF
        # if the 's' key is pressed, save the cropped region as a new image
        if key == ord("s"):
            cv.imwrite(FILE_NAME[:-4]+"_crop"+".png", clip)
            print("You saved a clip!")
        # if the esc key is pressed, break from the loop
        elif key == 27:
            cv.destroyWindow('Clipping')
            break


os.chdir(original_dir)
cv.destroyAllWindows()


