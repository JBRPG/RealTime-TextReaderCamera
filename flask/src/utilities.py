def get_file_path(file_name):
    import os
    import sys
    dir_path = os.path.dirname(sys.argv[0])
    return os.path.join(dir_path, file_name)
    # return file_name

def get_text_from_image_from_file(image_path):
    import pytesseract
    from PIL import Image
    imgD = Image.open(get_file_path(image_path))
    tessdata_dir_config = '--psm 10 --oem 1'  # 7 seems promising
    ocrText = pytesseract.image_to_string(imgD, config=tessdata_dir_config) #, config='-psm 6'
    return ocrText.strip()