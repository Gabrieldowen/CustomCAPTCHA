# This file is used to test if flask is working on your machine

# RUN THESE COMMANDS IN CMD LINE:
# 1: Step into FlaskEnvironment directory
# 2: run this without quotes "export FLASK_APP=FlaskTest.py"
# 3: "flask run"
# then paste URL into browser to see it running

import os
import random
from PIL import Image

objs = []   # The values for the correct objects
clues = [] # Paths to the two selected clues
images = [] # List of images in grid
solution = []

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

# Select the images that will be used in the CAPTCHA
def select_clues():
    global objs # Use the global variable for objs
    global clues    # Use the global variable
    objs = select_objects() # Select the objects
    clue1_dir = f'static/images/single/{objs[0]}'   # Path to directory of first clue options
    clue2_dir = f'static/images/single/{objs[1]}'   # Path to dir of second clue options
    single_imgs1 = [f for f in os.listdir(clue1_dir) if f.endswith('.png')] # Get all images in clue1_dir
    single_imgs2 = [f for f in os.listdir(clue2_dir) if f.endswith('.png')] # Get all images in clue2_dir
    clues.append(f'images/single/{objs[0]}/{single_imgs1[random.randint(0, len(single_imgs1) - 1)]}')    # Get random clue 1
    clues.append(f'images/single/{objs[1]}/{single_imgs2[random.randint(0, len(single_imgs2) - 1)]}')    # Get random clue 2

def select_images():
    global images
    select_clues()
    prefix = "images/multi" # Prefix for directory
    all_dirs = os.listdir(f'static/{prefix}')   # Get all directories in 'static/images/multi/'

    # Get the correct images

    correct_dirs = [x for x in all_dirs if str(objs[0]) in x and str(objs[1]) in x] # Get the directories containing the correct images
    correct = []    # List of correct images
    imgs1 = [f for f in os.listdir(f'static/{prefix}/{correct_dirs[0]}') if f.endswith('.png')]
    imgs2 = [f for f in os.listdir(f'static/{prefix}/{correct_dirs[1]}') if f.endswith('.png')]
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
    inc_imgs1 = [f for f in os.listdir(f'static/{prefix}/{incorrect_dirs[0]}') if f.endswith('.png')]
    inc_imgs2 = [f for f in os.listdir(f'static/{prefix}/{incorrect_dirs[1]}') if f.endswith('.png')]
    num_incorrect = 9 - num_correct # Select the remaining images as incorrect

    for i in range(num_incorrect):
        choice = random.randint(0,1)    # Choose which image list to choose from
        if choice == 0:
            rand = random.randint(0, len(inc_imgs1) - 1)
            if inc_imgs1[rand] not in incorrect:
                incorrect.append(f'{prefix}/{incorrect_dirs[0]}/{inc_imgs1[rand]}')
        else:
            rand = random.randint(0, len(inc_imgs2) - 1)
            if inc_imgs2[rand] not in incorrect:
                incorrect.append(f'{prefix}/{incorrect_dirs[1]}/{inc_imgs2[rand]}')

    images = correct + incorrect
# End select_images

def generate_captcha():
    image_files = [f for f in os.listdir('static/NineImageTest') if f.endswith('.png')]
    if len(image_files) < 9:
        return None

    selected_images = random.sample(image_files, 9)
    correct_index = random.randint(0, 8)
    correct_image = selected_images[correct_index]
    code = os.path.splitext(correct_image)[0]
    return code, selected_images, correct_index

# Flask stuff

from flask import Flask, render_template
app = Flask(__name__)
if __name__ =='__main__':
    app.run(debug=True)

@app.route('/')
def home():
    #return render_template("index.html")   
    captcha_code, selected_images, correct_index = generate_captcha()
    if not captcha_code:
        return 'Not enough captcha images found.'

    return render_template('index.html', captcha_code=captcha_code, selected_images=selected_images,
                           correct_index=correct_index)

@app.route('/validate', methods=['POST'])
def validate():
    # Your validation logic here
    print("validating")
    pass
