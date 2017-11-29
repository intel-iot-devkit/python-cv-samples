import numpy as np
import cv2
import copy

cap = cv2.VideoCapture('vtest.avi')
#pip install opencv-contrib-python
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

#number of frames is a variable for development purposes, you can change the for loop to a while(cap.isOpened()) instead to go through the whole video
num_frames = 350

first_iteration_indicator = 1
for i in range(0,num_frames):
    '''
    There are some important reasons this if statement exists:
        -in the first run there is no previous frame, so this accounts for that
        -the first frame is saved to be used for the overlay after the accumulation has occurred
        -the height and width of the video are used to create an empty image for accumulation (accum_image)
    '''
    if (first_iteration_indicator == 1):
        ret, frame = cap.read()
        first_frame = copy.deepcopy(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height, width = gray.shape[:2]
        accum_image = np.zeros((height,width), np.uint8)
        first_iteration_indicator = 0
        previous_frame = copy.deepcopy(gray)
    else:
        ret, frame = cap.read() #read a frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  #convert to grayscale

        fgmask = fgbg.apply(gray)   #remove the background

        #for testing purposes, show the result of the background subtraction
        # cv2.imshow('diff-bkgnd-frame', fgmask)

        # apply a binary threshold only keeping pixels above thresh and setting the result to maxValue.  If you want
        # motion to be picked up more, increase the value of maxValue.  To pick up the least amount of motion over time, set maxValue = 1
        thresh = 2
        maxValue = 2
        ret, th1 = cv2.threshold(fgmask, 2, 2, cv2.THRESH_BINARY)
        #for testing purposes, show the threshold image
        #cv2.imwrite('diff-th1.jpg', th1)

        #add to the accumulated image
        accum_image = cv2.add(accum_image, th1)
        #for testing purposes, show the accumulated image
        #cv2.imwrite('diff-accum.jpg', accum_image)

        #for testing purposes, control frame by frame
        # raw_input("press any key to continue")

        previous_frame = copy.deepcopy(gray)

    #for testing purposes, show the current frame
    # cv2.imshow('frame', gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    previous_frame = copy.deepcopy(gray)

# apply a color map
# COLORMAP_PINK also works well, COLORMAP_BONE is acceptable if the background is dark
color_image = im_color = cv2.applyColorMap(accum_image, cv2.COLORMAP_HOT)
# for testing purposes, show the colorMap image
#cv2.imwrite('diff-color.jpg', color_image)

#overlay the color mapped image to the first frame
result_overlay = cv2.addWeighted(first_frame, 0.7, color_image, 0.7, 0)

#save the final overlay image
cv2.imwrite('diff-overlay.jpg', result_overlay)

#cleanup
cap.release()
cv2.destroyAllWindows()