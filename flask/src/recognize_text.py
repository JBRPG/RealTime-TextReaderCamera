import numpy as np
import cv2 as cv
import pytesseract
import math
try:
    from src.utilities import get_file_path
    from src.transform import four_point_transform
except:
    from utilities import get_file_path
    from transform import four_point_transform
lower_case = 'abcdefghijklmnopqrstuvwxyz'
upper_case = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# tessdata_dir_config = '--psm 10 --oem 1 -c tessedit_char_whitelist=' + lower_case
tessdata_dir_config = '--psm 10 --oem 1 -c tessedit_char_whitelist=' + upper_case
# tessdata_dir_config = '--psm 10 --oem 1 -c tessedit_char_whitelist=' + upper_case + lower_case


def crop_and_simplify(img, rect):
    cropped = four_point_transform(img.copy(), rect)
    w = cropped.shape[0]
    h = cropped.shape[1]
    a = cropped[4:h-4, 4:w-4]
    gray = cv.split(cropped)[2]
    _retval, bin = cv.threshold(gray, 120, 255, cv.THRESH_BINARY)
    kernel = np.ones((1,1), np.uint8)
    b = cv.erode(bin, kernel, iterations=1)
    b = cv.merge([b, b, b])
    kernel = np.ones((3,3), np.uint8)
    c = cv.erode(bin, kernel, iterations=1)
    c = cv.merge([c, c, c])
    return [a, b, c]

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def is_same_shape(a, b):
    from shapely.geometry import Polygon
    p1 = Polygon(a)
    p2 = Polygon(b)
    threshold = 0.4
    is_same_size = (p1.area / p2.area > threshold) and (p2.area / p1.area > threshold)
    return p1.intersects(p2) and is_same_size

def find_squares(img):
    img = cv.GaussianBlur(img, (5, 5), 0)
    squares = []
    for gray in cv.split(img):
        for thrs in range(0, 255, 26):
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
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in range(4)])
                    if max_cos < 0.1:
                        is_duplicate = False
                        for square in squares:
                            is_duplicate = is_same_shape(square, cnt)
                            if is_duplicate:
                                break
                        if not is_duplicate:
                            squares.append(cnt)
    return squares


def read_letter(img, rect, save=False):
    images = crop_and_simplify(img, rect)
    for image in images:
        ocrText = pytesseract.image_to_string(image, config=tessdata_dir_config) #, config='-psm 6'
        ocrText = ocrText.strip()
        x1, y1 = rect[0]
        if len(ocrText) == 1:
            print(ocrText, (x1, y1))
            file_name = 'results/tiles_cropped_{0}_{1}.jpg'.format(x1, y1)
        else:
            file_name = 'results/tiles_cropped_{0}_{1}_bad.jpg'.format(x1, y1)
        # print(ocrText, x1)

        if save:
            print('saving:', file_name),
            cv.putText(image, ocrText,(0,20),cv.FONT_HERSHEY_COMPLEX,0.7,(255,0,0),1,cv.LINE_AA)
            cv.imwrite(get_file_path(file_name), image)

        if len(ocrText) == 1:
            return ocrText, str(x1).zfill(3) + '_' + str(y1).zfill(3)
        #else:
        #    print('Trying again...')

def get_letters_from_image(img_path, debug=False):
    img = cv.imread(img_path)
    squares = find_squares(img)
    print(len(squares), 'squares found')
    letter_map = {}
    for square in squares[1:]:
        result = read_letter(img, square, save=debug)
        if result:
            letter_map[result[1]] = result[0]
    letters = []
    for key in sorted(letter_map.keys()) :
        letters.append(letter_map[key])
    if debug:
        cv.drawContours( img, squares, -1, (255, 30, 0), 3 )
        cv.imwrite(get_file_path("results/tiles_outlined.jpg"), img)
    print(letter_map)
    return letters
