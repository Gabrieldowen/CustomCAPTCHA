# This is a script for generating images with the OpenAI DALL E api
from base64 import b64decode
import openai
import os
from pathlib import Path
import sys

# ----- Global Variables -----

# List of objects that will appear in the images
objects = ["a car", "a dog", "a rocket", "a computer", "a t-rex", "a map"]
# List of backgrounds for the images
backgrounds = ["the ocean", "outer space", "a rainforest", "a city"]
# List of different styles
styles = ["cartoonish", "historic", "surreal"]

# The environment variable for the OpenAI api key stored on local machine (On POSIX, use `export OPENAI_API_KEY="<your-key-value-here>"`)
openai.api_key = os.getenv("OPENAI_API_KEY")

# ----- Functions -----

# Decode the base64 string from a json file to a png
def decode(response, is_multi, args):
    # Make the first part of the image's filename the values of the arguments
    filename = ''.join(str(s) for s in args)

    # is_multi indicates whether it is a multi object image or not
    # If it is multi object, save it to a 'multi' subdirectory
    if is_multi == True:
        IMAGE_DIR = Path.cwd() / "images" / "multi" / filename
    # Else, save it to a 'single' subdirectory
    else:
        IMAGE_DIR = Path.cwd() / "images" / "single" / filename

    # Create an images directory if one doesn't exist
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    # Decode the base64 to png and save as a file
    for index, image_dict in enumerate(response["data"]):
        image_data = b64decode(image_dict["b64_json"])
        image_file = IMAGE_DIR / f"{filename}-{response['created']}-{index}.png"
        with open(image_file, mode="wb") as png:
            png.write(image_data)

# Generate images with three objects in them
def generate_multiobj(args):
    # The prompt for the image generation
    PROMPT = f"A {styles[args[1]]} image containing {objects[args[2]]}, {objects[args[3]]}, and {objects[args[4]]} located in {backgrounds[args[5]]}."

    # Loop to generate num_iter number of images
    for i in range(0, args[0]):
        # The json response for the generated image
        response = openai.Image.create(
            prompt=PROMPT,
            n=1,
            size="256x256",
            response_format = "b64_json",
        )
        # Decode the json response and save as a png file (with flag for `multi` set to True)
        decode(response, True, args)

# Generate images with only one object
def generate_singleobj(args):
    # The prompt for the image generation
    PROMPT = f"A {styles[args[1]]} image containing {objects[args[2]]} located in {backgrounds[args[3]]}."

    # Loop to generate num_iter number of images
    for i in range(0, args[0]):
        # The json response for the generated image
        response = openai.Image.create(
            prompt=PROMPT,
            n=1,
            size="256x256",
            response_format = "b64_json",
        )
        # Decode the json response and save as a png file (with flag for `multi` set to False)
        decode(response, False, args)

# The main driver function
def main():
    # Get runtime arguments
    func = sys.argv[1]  # Specify which function to use
    argv = sys.argv[2:] # Specify the arguments for the functions
    args = [eval(i) for i in argv]  # Cast the arguments to integers

    # If the specified function is `multi`, generate multi object images
    if func == "multi":
        generate_multiobj(args)
    # If the specified function is `single`, generate a single object image
    elif func == "single":
        generate_singleobj(args)
    # If invalid number of runtime args, print an error
    else:
        print("Invalid number of arguments", file=sys.stderr)


main()