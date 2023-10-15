# This is a script for generating images with the OpenAI DALL E api
from decode import decode   # User create library
import json
import os
import openai
from pathlib import Path
import sys

# List of objects that will appear in the images
objects = ["a car", "a dog", "a rocket", "a computer", "a t-rex", "a map"]
# List of backgrounds for the images
backgrounds = ["the ocean", "outer space", "a rainforest", "a city"]
# List of different styles
styles = ["cartoonish", "historic", "surreal"]

# The environment variable for the OpenAI api key stored on local machine (On POSIX, use `export OPENAI_API_KEY="<your-key-value-here>"`)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Generate images with three objects in them
def generate_multiobj(num_iter, idxs, idx1, idx2, idx3, idxbg):
    # The prompt for the image generation
    PROMPT = f"A {styles[idxs]} image containing {objects[idx1]}, {objects[idx2]}, and {objects[idx3]} located in {backgrounds[idxbg]}."
    # The directory to store the json responses for multi obj images
    DATA_DIR = Path.cwd() / "json_responses" / "multi"
    # Make the directory if it doesn't exist
    DATA_DIR.mkdir(exist_ok=True)

    # Loop to generate num_iter number of images
    for i in range(0, num_iter):
        # The json response for the generated image
        response = openai.Image.create(
            prompt=PROMPT,
            n=1,
            size="256x256",
            response_format = "b64_json",
        )

        # The name of the json file that will be saved
        filename = DATA_DIR / f"{PROMPT[:50]}-{response['created']}.json"
        # Write the json response to a file as base64
        with open(filename, mode="w", encoding="utf-8") as file:
            json.dump(response,file)
        # Decode the base64 image in the json to a png (with flag to indicate its a multi obj image)
        decode(filename, True)

# Generate images with only one object
def generate_singleobj(num_iter, idxs, idx1, idxbg):
    # The prompt for the image generation
    PROMPT = f"A {styles[idxs]} image containing {objects[idx1]} located in {backgrounds[idxbg]}."
    # The directory to store the json responses for single obj images
    DATA_DIR = Path.cwd() / "json_responses" / "single"
    # Make the directory if it doesn't exist
    DATA_DIR.mkdir(exist_ok=True)

    # Loop to generate num_iter number of images
    for i in range(0, num_iter):
        # The json response for the generated image
        response = openai.Image.create(
            prompt=PROMPT,
            n=1,
            size="256x256",
            response_format = "b64_json",
        )

        # The name of the json file that will be saved
        filename = DATA_DIR / f"{PROMPT[:75]}-{response['created']}.json"
        # Write the json response to a file as base64
        with open(filename, mode="w", encoding="utf-8") as file:
            json.dump(response,file)
        # Decode the base64 image in the json to a png (without flag for multi obj image)
        decode(filename, False)


# Get arguments passed at runtime and cast to integers
argv = sys.argv[1:]
args = [eval(i) for i in argv]

# If there are 6 runtime args, generate multi object images
if len(args) == 6:
    generate_multiobj(args[0], args[1], args[2], args[3], args[4], args[5])
# If 4 runtime args, generate a single object image
elif len(args) == 4:
    generate_singleobj(args[0], args[1], args[2], args[3])
# If invalid number of runtime args, print an error
else:
    print("Invalid number of arguments", file=sys.stderr)