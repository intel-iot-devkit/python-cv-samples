'''
Copyright (c) 2017 Intel Corporation.
Licensed under the MIT license. See LICENSE file in the project root for full license information.
'''

import copy
import cv2
import numpy as np


def main():
    """
    This method is used to see movement patterns over time. It creates a heatmap of the movements.
    For example, it could be used to see the usage of entrances to a factory floor over time,
    or patterns of shoppers in a store.
    """
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    out = cv2.VideoWriter('motion_heatmap_output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (int(cap.get(3)), int(cap.get(4))))
    # out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), 40, (int(cap.get(3)), int(cap.get(4)))) # Also works
    fgbg = cv2.createBackgroundSubtractorMOG2()

    first_iteration_indicator = 1

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            '''
            There are some important reasons this if statement exists:
                -in the first run there is no previous frame, so this accounts for that
                -the first frame is saved to be used for the overlay after the accumulation has occurred
                -the height and width of the video are used to create an empty image for accumulation (accum_image)
            '''

            if first_iteration_indicator == 1:
                first_frame = copy.deepcopy(frame)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                height, width = gray.shape[:2]
                accum_image = np.zeros((height, width), np.uint8)
                first_iteration_indicator = 0
            else:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert to grayscale
                fgmask = fgbg.apply(gray)  # remove the background
                cv2.imshow('diff-bkgnd-frame', fgmask)  # result of the background subtraction

                # apply a binary threshold only keeping pixels above thresh and setting the result to maxValue.
                # If you want motion to be picked up more, increase the value of maxValue.
                # To pick up the least amount of motion over time, set maxValue = 1
                thresh = 1
                max_value = 5
                ret, th_img = cv2.threshold(fgmask, thresh, max_value, cv2.THRESH_BINARY)

                # add to the accumulated image
                accum_image = cv2.add(accum_image, th_img)
                cv2.imshow('diff-accum', accum_image)  # accumulated frame

            cv2.imshow('frame', gray)  # current frame

            # apply a color map
            # COLORMAP_PINK also works well, COLORMAP_BONE is acceptable if the background is dark
            color_image = cv2.applyColorMap(accum_image, cv2.COLORMAP_INFERNO)
            cv2.imshow('diff-color', color_image)  # colorMap frame

            # overlay the color mapped image to the first frame
            result_overlay = cv2.addWeighted(first_frame, 0.7, color_image, 0.7, 0)
            cv2.imshow('diff-overlay', result_overlay)  # final overlay frame
            cv2.imwrite('diff-overlay.png', result_overlay)  # final overlay image
            out.write(result_overlay)
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        ch_ = cv2.waitKey(1)
        if ch_ == 27 or ch_ == ord('q') or ch_ == ord('Q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
