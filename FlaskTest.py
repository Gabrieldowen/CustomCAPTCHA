# This file is used to test if flask is working on your machine

# RUN THESE COMMANDS IN CMD LINE:
# 1: Step into FlaskEnvironment directory
# 2: run this without quotes "export FLASK_APP=FlaskTest.py"
# 3: "flask run"
# then paste URL into browser to see it running


from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def home():
    return render_template("index.html")

