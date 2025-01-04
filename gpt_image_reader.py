#This sends an image to chat gpt and asks it to describe the image. 
from key import API_KEY
import openai
import base64


image_path = "C:/Users/kahin/Downloads/16-af0075cl_1735282644.png"
with open(image_path, 'rb') as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()


model = "gpt-4o-mini"
prompt = "Tell me a joke"

client = openai.OpenAI(api_key=API_KEY)

#response = client.chat.completions.create(
#    model=model,
#    messages=[
#        {"role": "system", "content": "You are a helpful assistant."},
#        {"role": "user", "content": prompt}
#    ]
#)

#Add the image content to payload
response= client.chatt.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
        {"role": "user", "content": encoded_image}
    ]
)



# Extract and return the response content

print(response.choices[0].message.content.strip())