# Convert the json responses from the OpenAI image generation to png files
import json
from base64 import b64decode
from pathlib import Path
import sys

# Get the directory with the json files
DATA_DIR = Path.cwd() / "json_responses"https://urldefense.com/v3/__https://signup.azure.com/studentverification?offerType=1__;!!GNU8KkXDZlD12Q!4NF7nrnMUl3kvIJB_K9du2iuiW75D6fMTaz95rTy4TNro-s3-TSeU3JEO63hjfc5T1hLnjvMQW1PACFWXjujk7uUEn-huurSkB8$
# Pass the filename at runtime
JSON_FILE = DATA_DIR / sys.argv[1]
IMAGE_DIR = Path.cwd() / "images"

# Create an images directory if one doesn't exist
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

with open(JSON_FILE, mode="r", encoding="utf-8") as file:
    response = json.load(file)

for index, image_dict in enumerate(response["data"]):
    image_data = b64decode(image_dict["b64_json"])
    image_file = IMAGE_DIR / f"{JSON_FILE.stem}-{index}.png"
    with open(image_file, mode="wb") as png:
        png.write(image_data)