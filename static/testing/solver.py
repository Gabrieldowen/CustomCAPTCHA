from pathlib import Path
import cv2

# Get the paths to the images in the Downloads folder
def get_images():
    downloads_path = str(Path.home() / 'Downloads')
    captcha_path = f'{downloads_path}/CAPTCHA.png'    # Path to the grid image
    clue1_path = f'{downloads_path}/clue1.png'        # Path to the first clue
    clue2_path = f'{downloads_path}/clue2.png'        # Path to the second clue

    return [captcha_path, clue1_path, clue2_path]
# End get_images

# Open the images with cv2
def open_images(catpcha, clue1, clue2):
    cap_img = cv2.imread(catpcha)
    c1_img = cv2.imread(clue1)
    c2_img = cv2.imread(clue2)

    return [cap_img, c1_img, c2_img]
# End open_images

# Delete images from dowloads when done
def delete_images(cap_path, c1_path, c2_path):
    Path.unlink(cap_path)
    Path.unlink(c1_path)
    Path.unlink(c2_path)
# End delete_images

cap,c1,c2 = get_images()
#open_images(cap, c1, c2)
delete_images(cap, c1, c2)