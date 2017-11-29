# Analog Gauge Reader

This sample application takes an image or frame of an analog gauge an reads the value using computer vision.
It consists of two parts, the calibration, and the measurement.  During calibration the user gives it an image 
of the gauge to calibrate, and it prompts the user to enter the range of values in degrees.  It then uses these 
calibrated values in the measurement stage to convert the angle of the dial into a meaningful value.

## What you’ll learn
  * Circle detection
  * Line detection

## Gather your materials
  *	Python 2.7 or greater
  * OpenCV version 3.3.0 or greater
  *	A picture of a gauge to try (or you can use the sample one provided)

## Setup
1. Take a picture of a gauge or use the gauge-1.jpg provided.  If you name it something other than gauge-1.jpg make sure to
change that in the main() function.
2. Run the application (download the .zip at the end of this article first) and enter the requested values, using the output file gauge-#-calibration.jpg to determine the values. Here's an example of what the calibration image looks like:
[](/images/calibration-image.jpg)

For the calibration image above, you would enter in the following values:
[](/images/screen-prompt.jpg)

3.  The application by default reads the value of the gauge of the image you used for calibration.  For the provided image, here's what it reads:
[](/images/screen-output.jpg)

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

