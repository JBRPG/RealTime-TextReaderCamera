# https://hub.packtpub.com/opencv-detecting-edges-lines-shapes/
from utilities import get_file_path
from PIL import Image
import math
import cv2
import numpy as np
import pytesseract

balloons = cv2.imread(get_file_path('balloons.jpg'))
gray_img = cv2.cvtColor(balloons, cv2.COLOR_BGR2GRAY)
img = cv2.medianBlur(gray_img, 5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(
    img,cv2.HOUGH_GRADIENT,1,120, param1=100,param2=30,minRadius=0,maxRadius=0)

circles = np.uint16(np.around(circles))

for i in circles[0,:]:
   # draw the outer circle
   cv2.circle(balloons,(i[0],i[1]),i[2],(0,255,0),2)
   # draw the center of the circle
   cv2.circle(balloons,(i[0],i[1]),2,(0,0,255),3)

cv2.imwrite(get_file_path("balloons_circles.jpg"), balloons)
cv2.imshow("HoughCirlces", balloons)
cv2.waitKey()
cv2.destroyAllWindows()