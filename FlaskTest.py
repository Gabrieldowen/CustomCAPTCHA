# This file is used to test if flask is working on your machine

# RUN THESE COMMANDS IN CMD LINE:
# 1: Step into FlaskEnvironment directory
# 2: run this without quotes "export FLASK_APP=FlaskTest.py"
# 3: "flask run"
# then paste URL into browser to see it running
import json
import os
import random
from time import sleep
from unittest import result
from PIL import Image
import numpy as np
import cv2
import base64
import io
from flask import Flask, render_template, request, redirect, url_for


dim = 450   # The dimensions of the large image

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
    correct = set()    # Set of correct images (only unique images)
    imgs1 = [f for f in os.listdir(f'{prefix}/{correct_dirs[0]}') if f.endswith('.png')]
    imgs2 = [f for f in os.listdir(f'{prefix}/{correct_dirs[1]}') if f.endswith('.png')]
    num_correct = random.randint(3,6)   # Select a random number of correct images from both directories (between 3 and 6 images)

    while len(correct) < num_correct:
        choice = random.randint(0,1)    # Choose which image list to choose from
        if choice == 0:
            rand = random.randint(0, len(imgs1) - 1)    # Random index
            correct.add(f'{prefix}/{correct_dirs[0]}/{imgs1[rand]}')    # Add image to correct images set
        else:
            rand = random.randint(0, len(imgs2) - 1)    # Random index
            correct.add(f'{prefix}/{correct_dirs[1]}/{imgs2[rand]}')    # Add image to correct images set

    # Get the incorrect images

    incorrect_dirs = [x for x in all_dirs if x not in correct_dirs] # Get the directories for incorrect images
    incorrect = set()  # Set of incorrect images (only unique images)
    inc_imgs1 = [f for f in os.listdir(f'{prefix}/{incorrect_dirs[0]}') if f.endswith('.png')]
    inc_imgs2 = [f for f in os.listdir(f'{prefix}/{incorrect_dirs[1]}') if f.endswith('.png')]
    num_incorrect = 9 - num_correct # Select the remaining images as incorrect

    while len(incorrect) < num_incorrect:
        choice = random.randint(0,1)    # Choose which image list to choose from
        if choice == 0:
            rand = random.randint(0, len(inc_imgs1) - 1)
            incorrect.add(f'{prefix}/{incorrect_dirs[0]}/{inc_imgs1[rand]}')    # Add image to incorrect images set
        else:
            rand = random.randint(0, len(inc_imgs2) - 1)
            incorrect.add(f'{prefix}/{incorrect_dirs[1]}/{inc_imgs2[rand]}')    # Add image to incorrect images set

    return [list(correct) + list(incorrect), list(np.arange(0,num_correct))]    # Return the list of all images, as well as a list of the indices of correct images
# End select_images

# Create a random order for the images to appear in the CAPTCHA
def scramble_images():
    idx = list(np.arange(0,9))  # Make a list 0..8 that marks the indices of the images in the images list
    np.random.shuffle(idx)  # Shuffle the indices of this indices list
    # i.e. If the shuffled list is [1, 6, 8, 0, 5, 4, 7, 2, 3], then the image at index 0 in the images list will be at index 3 in the CAPTCHA
    # because 0 is at index 3. Further, the image at index 1 in the images list will be at index 0 in the CAPTCHA
    return idx
# End scramble_images

# Combine smaller, individual images into one larger one
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

    return full_img.resize((dim,dim))   # Resize the image to dim px x dim px and return
# End combine_images

# Add noise to image
def add_noise(image):
    img = np.array(image)   # Convert image to an array
    uniform_noise = np.zeros((dim, dim, 3), dtype=np.uint8) # Create an array of zeros of the same dimensions as 'img'
    cv2.randu(uniform_noise, 0, 255)    # Create random uniform noise in 'uniform_noise'
    uniform_noise = (uniform_noise*0.75).astype(np.uint8)    # Reduce amount of noise
    un_img = cv2.add(img, uniform_noise)    # Add noise to 'img' array

    return Image.fromarray(un_img)  # Return array as image
# End add_noise


# Flask stuff

app = Flask(__name__)
if __name__ =='__main__':
    app.run(debug=True, host='0.0.0.0')

"""
@app.route('/')
def home():
    # return render_template("index.html")
    # captcha_code, selected_images, correct_index = generate_captcha(objs)
    # if not captcha_code:
        # return 'Not enough captcha images found.'

    objs = select_objects()
    clues = select_clues(objs)
    return render_template('index.html', selected_images=select_images(objs, clues))
"""

@app.route('/')
def home():
    # Get the images for the CAPTCHA
    global key
    global idx
    objs = select_objects()
    clues = select_clues(objs)
    images, key = select_images(objs, clues)
    idx = scramble_images()

    grid_img = combine_images(images, idx)  # Combine the images into one
    grid_img = add_noise(grid_img)  # Add noise

    data = io.BytesIO()    # Buffer to save openned image 'grid_img' in memory
    grid_img.save(data, 'PNG')  # Save to memory buffer as png
    encoded_img = base64.b64encode(data.getvalue()) # Encode to base-64

    print(idx)
    print(key)
    return render_template('index.html', img_data=encoded_img.decode('utf-8'), clues=clues)   # Send image to html as utf-8




@app.route('/validate', methods=['POST'])
def validate():

    if request.form.get('honeypot'):
         # It's likely a bot, handle accordingly (e.g., log, block, etc.)
        print("BOT LIKELY")
        return redirect(url_for('home'))

    # Your validation logic here
    Submission = request.form.get('selectedButtons', '[]')
    Submission = Submission.replace('"', '').replace("'", '').replace(",", '').replace("[", '').replace("]", '')

    # Formats the answer key to style of submission
    AnswerKey = ""
    print(f'idx {idx}')
    for index, item in enumerate(idx):
        if item in key:
            AnswerKey += '1'
        else:
            AnswerKey += '0'

    # checks if submission == key
    print(f'sub {Submission}')
    print(AnswerKey)
    if Submission == AnswerKey:
        return render_template('success.html')

    return redirect(url_for('home'))

#END VALIDATE()

# TEST CODE
"""
objs = select_objects()
clues = select_clues(objs)
images, correct = select_images(objs, clues)
idx = scramble_images()
print(images, idx)


test = combine_images(images, idx)
test = add_noise(test)

test.show()
"""