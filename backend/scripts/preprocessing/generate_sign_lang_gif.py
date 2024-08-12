from PIL import Image
import matplotlib.pyplot as plt

# Define the path to your sign language alphabet images folder
images_folder = r'YOUR/IMAGE_FOLDER/PATH'

# Define a mapping from text to image filenames
sign_language_dict = {
    'A': 'A.png',
    'B': 'B.png',
    'C': 'C.png',
    'D': 'D.png',
    'E': 'E.png',
    'F': 'F.png',
    'G': 'G.png',
    'H': 'H.png',
    'I': 'I.png',
    'J': 'J.png',
    'K': 'K.png',
    'L': 'L.png',
    'M': 'M.png',
    'N': 'N.png',
    'O': 'O.png',
    'P': 'P.png',
    'Q': 'Q.png',
    'R': 'R.png',
    'S': 'S.png',
    'T': 'T.png',
    'U': 'U.png',
    'V': 'V.png',
    'W': 'W.png',
    'X': 'X.png',
    'Y': 'Y.png',
    'Z': 'Z.png',
    ' ': 'space.png',  # Define a blank image for spaces
}

# Function to translate text to sign language images
def text_to_sign_language(text):
    # Create a list to store the sign language images
    sign_language_images = []

    for letter in text.upper():
        if letter in sign_language_dict:
            image_path = images_folder + sign_language_dict[letter]
            try:
                img = Image.open(image_path)
                sign_language_images.append(img)
            except FileNotFoundError:
                print(f"Image not found for letter: {letter}")

    return sign_language_images

# Translate text to sign language images
text_to_translate = input("Enter text: ")
translated_images = text_to_sign_language(text_to_translate)

# Display the translated images as a GIF
translated_images[0].save('translated_sign_language.gif',
                          save_all=True, append_images=translated_images[1:], optimize=False, duration=500, loop=0)