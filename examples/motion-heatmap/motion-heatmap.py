# -*- coding: utf-8 -*-
"""
Copyright (c) 2017 Intel Corporation.
Licensed under the MIT license. See LICENSE file in the project root for full license information.
"""

import argparse
import cv2
import copy
import os
import numpy as np


def main():
    parser = argparse.ArgumentParser(
        description='Generate the heatmaps from a video', )

    parser.add_argument('-i',
                        '--input',
                        help='Path to video',
                        default='vtest.avi',
                        type=str,
                        dest='INPUT')
    parser.add_argument(
        '-f',
        '--frames',
        help=
        'Number of frames to go through. Default is 350, 0 is to go through full video (WARNING: this might take some time).',
        type=int,
        default=350,
        dest='NUM_FRAMES')
    parser.add_argument(
        '-p',
        '--progress-bar',
        help=
        'Display progress bar (requires tqdm, which can be installed with `pip install tqdm`.',
        type=bool,
        default=False,
        dest='PROGRESS_BAR')

    args = parser.parse_args()

    cap = cv2.VideoCapture(args.INPUT)
    # pip install opencv-contrib-python
    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

    # number of frames is a variable for development purposes,
    # you can change the for loop to a while(cap.isOpened()) instead to go through the whole video
    num_frames = args.NUM_FRAMES
    if num_frames == 0:
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    first_iteration_indicator = 1
    current_frame_number = 0

    if args.PROGRESS_BAR:
        from tqdm import trange
        iterate_through = trange(num_frames)
    else:
        iterate_through = range(0, num_frames)
    for i in iterate_through:
        """
        There are some important reasons this if statement exists:
            -in the first run there is no previous frame, so this accounts for that
            -the first frame is saved to be used for the overlay after the accumulation has occurred
            -the height and width of the video are used to create an empty image for accumulation (accum_image)
        """
        if (first_iteration_indicator == 1):
            ret, frame = cap.read()
            first_frame = copy.deepcopy(frame)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            height, width = gray.shape[:2]
            accum_image = np.zeros((height, width), np.uint8)
            first_iteration_indicator = 0
        else:
            ret, frame = cap.read()  # read a frame
            gray = cv2.cvtColor(frame,
                                cv2.COLOR_BGR2GRAY)  # convert to grayscale

            fgmask = fgbg.apply(gray)  # remove the background

            # for testing purposes, show the result of the background subtraction
            # cv2.imshow('diff-bkgnd-frame', fgmask)

            # apply a binary threshold only keeping pixels above thresh and
            # setting the result to maxValue.  If you want
            # motion to be picked up more, increase the value of maxValue.
            # To pick up the least amount of motion over time, set maxValue = 1
            thresh = 2
            maxValue = 2
            ret, th1 = cv2.threshold(fgmask, thresh, maxValue,
                                     cv2.THRESH_BINARY)
            # for testing purposes, show the threshold image
            # cv2.imwrite('diff-th1.jpg', th1)

            # add to the accumulated image
            accum_image = cv2.add(accum_image, th1)
            # for testing purposes, show the accumulated image
            # cv2.imwrite('diff-accum.jpg', accum_image)

            # for testing purposes, control frame by frame
            # raw_input("press any key to continue")

        # for testing purposes, show the current frame
        # cv2.imshow('frame', gray)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        current_frame_number += 1

    # apply a color map
    # COLORMAP_PINK also works well, COLORMAP_BONE is acceptable if the background is dark
    color_image = im_color = cv2.applyColorMap(accum_image, cv2.COLORMAP_HOT)
    # for testing purposes, show the colorMap image
    # cv2.imwrite('diff-color.jpg', color_image)

    # overlay the color mapped image to the first frame
    result_overlay = cv2.addWeighted(first_frame, 0.7, color_image, 0.7, 0)

    # Output filename generation
    head, tail = os.path.split(args.INPUT)
    # save the final overlay image
    cv2.imwrite('{}_overlay.jpg'.format(tail.split('.')[0]), result_overlay)

    # cleanup
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
