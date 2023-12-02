# This file is used to test if flask is working on your machine

# RUN THESE COMMANDS IN CMD LINE:
# 1: Step into FlaskEnvironment directory
# 2: run this without quotes "export FLASK_APP=FlaskTest.py"
# 3: "flask run"
# then paste URL into browser to see it running

import os
import random
from unittest import result
from PIL import Image

clues = [] # Paths to the two selected clues
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
    objs = select_objects() # Select the objects
    clue1_dir = f'static/images/single/{objs[0]}'   # Path to directory of first clue options
    clue2_dir = f'static/images/single/{objs[1]}'   # Path to dir of second clue options
    single_imgs1 = [f for f in os.listdir(clue1_dir) if f.endswith('.png')] # Get all images in clue1_dir
    single_imgs2 = [f for f in os.listdir(clue2_dir) if f.endswith('.png')] # Get all images in clue2_dir
    clues.append(f'images/single/{objs[0]}/{single_imgs1[random.randint(0, len(single_imgs1))]}')    # Get random clue 1
    clues.append(f'images/single/{objs[1]}/{single_imgs2[random.randint(0, len(single_imgs2))]}')    # Get random clue 2
    return generate_captcha(objs)



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
    captcha_code, selected_images, correct_index = select_clues()
    if not captcha_code:
        return 'Not enough captcha images found.'

    return render_template('index.html', captcha_code=captcha_code, selected_images=selected_images,
                           correct_index=correct_index)


@app.route('/validate', methods=['POST'])
def validate():
    # Your validation logic here
    print(request.form)
    print("validating")

    return redirect(url_for('home'))
