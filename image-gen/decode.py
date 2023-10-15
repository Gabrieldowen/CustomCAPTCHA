# Convert the json responses from the OpenAI image generation to png files
import json
from base64 import b64decode
from pathlib import Path

# Decode the base64 string from a json file to a png
def decode(JSON_FILE, is_multi):
    # is_multi indicates whether it is a multi object image or not
    # If it is multi object, save it to a 'multi' subdirectory
    if is_multi == True:
        IMAGE_DIR = Path.cwd() / "images" / "multi"
    # Else, save it to a 'single' subdirectory
    else:
        IMAGE_DIR = Path.cwd() / "images" / "single"

    # Create an images directory if one doesn't exist
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    # Load in the json file
    with open(JSON_FILE, mode="r", encoding="utf-8") as file:
        response = json.load(file)

    # Decode the base64 to png
    for index, image_dict in enumerate(response["data"]):
        image_data = b64decode(image_dict["b64_json"])
        image_file = IMAGE_DIR / f"{JSON_FILE.stem}-{index}.png"
        with open(image_file, mode="wb") as png:
            png.write(image_data)