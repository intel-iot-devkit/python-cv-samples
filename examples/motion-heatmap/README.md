# Motion Heatmap



## What you’ll learn
  * background subtraction
  * application of a threshold
  * accumulation of changed pixels over time
  * add a color/heat map

## Gather your materials
  *	Python 2.7 or greater
  * OpenCV version 3.3.0 or greater
  *	The vtest.avi video from https://github.com/opencv/opencv/blob/master/samples/data/vtest.avi

## Setup
1. Download the vtest.avi video from https://github.com/opencv/opencv/blob/master/samples/data/vtest.avi and put it in the same folder as the python script.
2. 

Original image:
[](/images/gauge-1.jpg)

## Get the Code
The application can be downloaded as a .zip at the end of this article.

## How it works
The main functions used in OpenCV are HoughCircles (to detect the outline of the gauge and center point) and HoughLines (to detect the dial).

Basic filtering is done as follows:
For cirles (this happens in calibrate_gauge() )
* only return circles from HoughCircles that are within reasonable range of the image height (this assumes the gauge takes up most of the view)
* average the resulting circles and use the average for the center point and radius
For lines (this happens in get_current_value() )
* apply a threshold using cv2.threshold.  cv2.THRESH_BINARY_INV with threshold of 175 and maxValue of 255 work fine
* remove all lines outside a given radius
* check if a line is within an acceptable range of the radius
* use the first acceptable line as the dial

There is a considerable amount of triginomotry involved to create the calibration image, mainly sin and cos to plot the calibration image lines and arctan to get the angle
of the dial.  This approach sets 0/360 to be the -y axis (if the image has a cartesian grid in the middle) and it goes clock-wise. There is a slight
modification to make the 0/360 degrees be at the -y axis, by an addition (i+9) in the calculation of p_text[i][j]. Without this +9 the 0/360 point would be on the +x axis.  So this
implementation assumes the gauge is aligned in the image, but it can be adjusted by changing the value of 9 to something else.

