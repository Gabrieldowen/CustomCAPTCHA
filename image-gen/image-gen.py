# This is a script for generating images with the OpenAI DALL E api
import json
import os
import openai
from pathlib import Path

# List of objects that will appear in the images
objects = ["a car", "a dog", "a rocket", "a computer", "a t-rex", "Abraham Lincoln"]
# List of backgrounds for the images
backgrounds = ["ocean", "outer space", "rainforest", "city"]

# The prompt for the image generation
PROMPT = f"an image of {objects[3]} and {objects[5]} with a background of {backgrounds[1]}"
# The directory to store the json responses
DATA_DIR = Path.cwd() / "json_responses"
# Make the directory if it doesn't exist
DATA_DIR.mkdir(exist_ok=True)

# The environment variable for the OpenAI api key stored on local machine
openai.api_key = os.getenv("OPENAI_API_KEY")

# The json response for the generated image
response = openai.Image.create(
    prompt=PROMPT,
    n=1,
    size="256x256",
    response_format = "b64_json",
)

# The name of the json file that will be saved
file_name = DATA_DIR / f"{PROMPT[:50]}-{response['created']}.json"
# Write the json response to a file
with open(file_name, mode="w", encoding="utf-8") as file:
    json.dump(response,file)