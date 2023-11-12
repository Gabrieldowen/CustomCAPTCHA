# This file is used to test if flask is working on your machine

# RUN THESE COMMANDS IN CMD LINE:
# 1: Step into FlaskEnvironment directory
# 2: run this without quotes "export FLASK_APP=FlaskTest.py"
# 3: "flask run"
# then paste URL into browser to see it running

import os
import random

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

    return render_template('sandbox.html', captcha_code=captcha_code, selected_images=selected_images,
                           correct_index=correct_index)

@app.route('/validate', methods=['POST'])
def validate():
    # Your validation logic here
    print("validating")
    pass

def generate_captcha():
    image_files = [f for f in os.listdir('static/SixImageTest') if f.endswith('.png')]
    if len(image_files) < 6:
        return None

    selected_images = random.sample(image_files, 6)
    correct_index = random.randint(0, 5)
    correct_image = selected_images[correct_index]
    code = os.path.splitext(correct_image)[0]
    return code, selected_images, correct_index
