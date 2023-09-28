# This file is used to test if flask is working on your machine

# RUN THESE COMMANDS IN CMD LINE:
# 1: Step into FlaskEnvironment directory
# 2: export FLASK_APP=FlaskTest.py
# 3: flask run
# then paste URL into browser to see it running


from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'This is Flask at work!'