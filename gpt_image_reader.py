#This sends an image to chat gpt and asks it to describe the image. 
import openai
import base64
from openai import OpenAI
import os
from dotenv import load_dotenv
import os

load_dotenv()

print(os.getenv("test_key"))

#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Set your OpenAI API key




image_path = "C:/Users/kahin/Downloads/16-af0075cl_1735282644.png"
with open(image_path, 'rb') as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()


model = "gpt-4o-mini"
prompt = "Tell me a joke"

client = openai.OpenAI(api_key=os.getenv("API_KEY"))
OpenAI.api_key = os.getenv("API_KEY")


print("Starting to send image to chat gpt")

#Add the image content to payload
#The response says that there are too many tokens needed to process the image.

#response= client.chat.completions.create(
#    model=model,
#    messages=[
#        {"role": "system", "content": "what is this image."},
#        {"role": "user", "content": prompt},
#        {"role": "user", "content": encoded_image},
#        {"max_tokens": 40000},
#    ]
#)


# Extract and return the response content
#print(response.choices[0].message.content.strip())

"""


# Load the image
with open(image_path, "rb") as image_file:
    response = client.chat.completions.create(
        model="gpt-4-vision",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What do you see in this image?"}
        ],
        files={"image": image_file}
    )


# Display the response
print(response['choices'][0]['message']['content'])
"""




# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Getting the base64 string
base64_image = encode_image(image_path)

response = client.chat.completions.create(
    model="gpt-4-vision-preview",
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