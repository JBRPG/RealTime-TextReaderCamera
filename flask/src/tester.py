from recognize_text import get_letters_from_image
from utilities import get_file_path
# image_path = get_file_path('images/tiles.png')
# image_path = get_file_path('images/christy1.jpg')
image_path = get_file_path('images/letters_2.jpg')
# image_path = get_file_path('images/letters_3.jpg')
image_path = get_file_path('images/test_image_i.png')
# letters = get_letters_from_image(image_path, debug=True)
letters = get_letters_from_image(image_path)
print(letters)
