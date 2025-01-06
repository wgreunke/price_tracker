#From https://platform.openai.com/docs/guides/vision/overview
#This sends an image to chat gpt and asks it to describe the image. 
import openai
import base64
from openai import OpenAI
import os
from dotenv import load_dotenv
import os

load_dotenv()

import base64
from openai import OpenAI

print("")
print("-------------")

client = OpenAI(api_key=os.getenv("API_KEY"))

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Path to your image
image_path = "16-af0075cl_1735282644.png"

# Getting the base64 string
base64_image = encode_image(image_path)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What is in this image?",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        }
    ],
)

print(response.choices[0])