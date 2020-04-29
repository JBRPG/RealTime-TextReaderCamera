# brew install tesseract
# pip install pytesseract

# tesseract letter_a.jpg output  -l eng --psm 10

import pytesseract
from PIL import Image

def get_file_path(file_name):
    import os
    import sys
    dir_path = os.path.dirname(sys.argv[0])
    return os.path.join(dir_path, file_name)

# imgD = Image.open(get_file_path('./letter_a.jpg'))
imgD = Image.open(get_file_path('./tiles.png'))
'''
image_to_string(image, lang=None, config='', nice=0, output_type='string', timeout=0)
    Returns the result of a Tesseract OCR run on the provided image to string
'''
tessdata_dir_config = '--psm 8 --oem 1'  # 7 seems promising
ocrText = pytesseract.image_to_string(imgD, config=tessdata_dir_config) #, config='-psm 6'
print(ocrText)
