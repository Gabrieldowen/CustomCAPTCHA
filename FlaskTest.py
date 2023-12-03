# This file is used to test if flask is working on your machine

# RUN THESE COMMANDS IN CMD LINE:
# 1: Step into FlaskEnvironment directory
# 2: run this without quotes "export FLASK_APP=FlaskTest.py"
# 3: "flask run"
# then paste URL into browser to see it running

import os
import random
from time import sleep
from unittest import result
from PIL import Image
import numpy as np



# Select the two objects that will be used in the CAPTCHA
def select_objects():
    obj1 = random.randint(0,3)  # Select random int
    obj2 = obj1
    while obj2 == obj1: # Loop until obj1 != obj2
        obj2 = random.randint(0,3)
    # Return the values such that it is in ascending order
    if obj1 < obj2:
        return [obj1, obj2]

    return [obj2, obj1]
# End select_objects


# Select the images that will be used in the CAPTCHA
def select_clues(objs):
    clues = []
    clue1_dir = f'static/images/single/{objs[0]}'   # Path to directory of first clue options
    clue2_dir = f'static/images/single/{objs[1]}'   # Path to dir of second clue options
    single_imgs1 = [f for f in os.listdir(clue1_dir) if f.endswith('.png')] # Get all images in clue1_dir
    single_imgs2 = [f for f in os.listdir(clue2_dir) if f.endswith('.png')] # Get all images in clue2_dir
    clues.append(f'images/single/{objs[0]}/{single_imgs1[random.randint(0, len(single_imgs1) - 1)]}')    # Get random clue 1
    clues.append(f'images/single/{objs[1]}/{single_imgs2[random.randint(0, len(single_imgs2) - 1)]}')    # Get random clue 2
    return clues
# End select_clues

def select_images(objs, clues):
    prefix = "static/images/multi" # Prefix for directory
    all_dirs = os.listdir(prefix)   # Get all directories in 'static/images/multi/'

    # Get the correct images

    correct_dirs = [x for x in all_dirs if str(objs[0]) in x and str(objs[1]) in x] # Get the directories containing the correct images
    correct = []    # List of correct images
    imgs1 = [f for f in os.listdir(f'{prefix}/{correct_dirs[0]}') if f.endswith('.png')]
    imgs2 = [f for f in os.listdir(f'{prefix}/{correct_dirs[1]}') if f.endswith('.png')]
    num_correct = random.randint(3,6)   # Select a random number of correct images from both directories (between 3 and 6 images)

    for i in range(num_correct):
        choice = random.randint(0,1)    # Choose which image list to choose from
        if choice == 0:
            rand = random.randint(0, len(imgs1) - 1)    # Random index
            if imgs1[rand] not in correct:  # Only add if it's not already selected
                correct.append(f'{prefix}/{correct_dirs[0]}/{imgs1[rand]}')
        else:
            rand = random.randint(0, len(imgs2) - 1)    # Random index
            if imgs2[rand] not in correct:  # Only add if not already select
                correct.append(f'{prefix}/{correct_dirs[1]}/{imgs2[rand]}')

    # Get the incorrect images

    incorrect_dirs = [x for x in all_dirs if x not in correct_dirs] # Get the directories for incorrect images
    incorrect = []  # List of incorrect images
    inc_imgs1 = [f for f in os.listdir(f'{prefix}/{incorrect_dirs[0]}') if f.endswith('.png')]
    inc_imgs2 = [f for f in os.listdir(f'{prefix}/{incorrect_dirs[1]}') if f.endswith('.png')]
    num_incorrect = 9 - num_correct # Select the remaining images as incorrect

    for i in range(num_incorrect):
        choice = random.randint(0,1)    # Choose which image list to choose from
        if choice == 0:
            rand = random.randint(0, len(inc_imgs1) - 1)
            if inc_imgs1[rand] not in incorrect:    # Only add if not already selected
                incorrect.append(f'{prefix}/{incorrect_dirs[0]}/{inc_imgs1[rand]}')
        else:
            rand = random.randint(0, len(inc_imgs2) - 1)
            if inc_imgs2[rand] not in incorrect:    # Only add if not already selected
                incorrect.append(f'{prefix}/{incorrect_dirs[1]}/{inc_imgs2[rand]}')

    return [correct + incorrect, list(np.arange(0,num_correct))]    # Return the list of all images, as well as a list of the indices of correct images
# End select_images

# Create a random order for the images to appear in the CAPTCHA
def scramble_images():
    idx = list(np.arange(0,9))  # Make a list 0..8 that marks the indices of the images in the images list
    np.random.shuffle(idx)  # Shuffle the indices of this indices list
    # i.e. If the shuffled list is [1, 6, 8, 0, 5, 4, 7, 2, 3], then the image at index 0 in the images list will be at index 3 in the CAPTCHA
    # because 0 is at index 3. Further, the image at index 1 in the images list will be at index 0 in the CAPTCHA
    return idx
# End scramble_images

def combine_images(images, idx):
    rows = []   # Rows of combines images

    # Create combine images into rows that will be combined into one full image
    for m in range(0,3):
        imgs = []   # Images open for this row
        for i in range(0+(m*3), 3+(m*3)):
            imgs.append(Image.open(images[idx[i]]))
        new_img = Image.new('RGB', (3*imgs[0].size[0], imgs[0].size[1]), (250, 250, 250))   # Create a new image with 3 * width of smaller image
        new_img.paste(imgs[0], (0,0))
        new_img.paste(imgs[1], (imgs[0].size[0], 0))
        new_img.paste(imgs[2], (2*imgs[0].size[0], 0))
        rows.append(new_img)

    # Combine rows together veritcally to create a square image containing all 9 small images
    full_img = Image.new('RGB', (rows[0].size[0], 3*rows[0].size[1]), (250, 250, 250))  # Create square image with dimmensions 3*image width x 3*image height
    full_img.paste(rows[0], (0,0))
    full_img.paste(rows[1], (0, rows[0].size[1]))
    full_img.paste(rows[2], (0, 2*rows[0].size[1]))

    return full_img.resize((450,450))   # Resize the image to 450px x 450px and return
# End combine_images

def generate_captcha(objs):

    CorrectOptions = [0, 1, 2, 3]
    CorrectOptions.remove(objs[0])
    CorrectOptions.remove(objs[1])

    pathFolder = ''.join(sorted(f'{objs[1]}' + f'{objs[0]}' + f'{random.choice(CorrectOptions)}'))
    CorrectImages = [f for f in os.listdir(f"static/images/multi/{pathFolder}/") if f.endswith('.png')]

    print(pathFolder)

    if len(CorrectImages) < 9:
        return None

    
    CaptchaImages = [f"images/multi/{pathFolder}/" + s for s in random.sample(CorrectImages, 9)]

    print(CaptchaImages)
    correct_index = random.randint(0, 8)
    correct_image = CaptchaImages[correct_index]
    code = os.path.splitext(correct_image)[0]
    return code, CaptchaImages, correct_index

# Flask stuff


from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)
if __name__ =='__main__':
    app.run(debug=True)


@app.route('/')
def home():
    # return render_template("index.html")
    # captcha_code, selected_images, correct_index = generate_captcha(objs)
    # if not captcha_code:
        # return 'Not enough captcha images found.'

    return render_template('index.html', selected_images=select_images(objs, clues))


@app.route('/validate', methods=['POST'])
def validate():
    # Your validation logic here
    Submission = request.form.get('selectedButtons', '[]')
    AnswerKey = '["0","0","0","0","0","0","0","0","0"]'

    if Submission == AnswerKey:
        print("correct")
    else:
        print("Wrong")

    return render_template('success.html')

# TEST CODE
objs = select_objects()
clues = select_clues(objs)
images, correct = select_images(objs, clues)
idx = scramble_images()
print(images, idx)

"""
test = combine_images(images, idx)

test.show()
"""