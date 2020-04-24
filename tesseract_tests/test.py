# brew install tesseract
# pip install pytesseract


import pytesseract
from PIL import Image

imgD = Image.open('./tiles.png')
ocrText = pytesseract.image_to_string(imgD) #, config='-psm 6'
print(ocrText)
