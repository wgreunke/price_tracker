#This sends an image to chat gpt and asks it to describe the image. 

import openai

client = openai.OpenAI()

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "image",
          "source": {
            "type": "base64",
            "media_type": "image/png",
            "data": encoded_image
          }
        }
      ]
    }
  ]
)