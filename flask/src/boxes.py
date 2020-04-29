from __future__ import print_function
import sys
xrange = range
import numpy as np
import cv2 as cv
from utilities import get_file_path, get_text_from_image_from_file
import pytesseract


tessdata_dir_config = '--psm 10 --oem 1'  # 7 seems promising

def get_bounds(squares):
    bounds = []
    for square in squares:
        x1, y1 = square[0]
        x2, y2 = square[0]
        for coord in square:
            if coord[0] < x1:
                x1 = coord[0]
            if coord[0] > x2:
                x2 = coord[0]
            if coord[1] < y1:
                y1 = coord[1]
            if coord[1] > y2:
                y2 = coord[1]
        bounds.append(((x1, y1), (x2, y2)))
    return bounds

def crop_image(img, rect, save=False):
    coord1, coord2 = rect
    x1, y1 = coord1
    x2, y2 = coord2
    cropped = img[y1:y2, x1:x2]
    file_name = 'results/tiles_cropped_{0}_{1}.jpg'.format(x1, y1)
    ocrText = pytesseract.image_to_string(cropped, config=tessdata_dir_config) #, config='-psm 6'
    print(ocrText.strip(), file_name)
    if save:
        cv.imwrite(get_file_path(file_name), cropped)

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
    img = cv.GaussianBlur(img, (5, 5), 0)
    squares = []
    for gray in cv.split(img):
        for thrs in xrange(0, 255, 26):
            if thrs == 0:
                bin = cv.Canny(gray, 0, 50, apertureSize=5)
                bin = cv.dilate(bin, None)
            else:
                _retval, bin = cv.threshold(gray, thrs, 255, cv.THRESH_BINARY)
            contours, _hierarchy = cv.findContours(bin, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv.arcLength(cnt, True)
                cnt = cv.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and cv.contourArea(cnt) > 1000 and cv.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                    if max_cos < 0.1:
                        squares.append(cnt)
    return squares




# executable code
from glob import glob
for fn in glob(get_file_path('images/tiles.png')):
    img = cv.imread(fn)
    squares = find_squares(img)
    bounds = get_bounds(squares)
    bounds = list(set(bounds))
    print(len(squares), 'detected')
    print(len(bounds), 'detected')
    for rect in bounds:
        crop_image(img, rect, save=True)
    cv.drawContours( img, squares, -1, (0, 255, 0), 3 )
    cv.imwrite(get_file_path("results/tiles_outlined.jpg"), img)
print('done!')