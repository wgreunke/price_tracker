#Claude 3.5 Sonnet with Bedrock and images
#https://medium.com/@codingmatheus/sending-images-to-claude-3-using-amazon-bedrock-b588f104424f
import base64
import json
import boto3

model_id="anthropic.claude-3-5-haiku-20241022-v1:0"

image_path = r"C:/Users/kahin/Downloads/16-af0075cl_1735282644.png"

#Load the image and decode it.
with open(image_path,"rb") as image_file:
    base64_image=base64.b64encode(image_file.read()).decode('utf-8')


#Define the payload
payload={
    "messages":[
        {
            "role":"user",
            "content":[
                {
                    "type":"image",
                    "source":{
                        "type":"base64",
                        "media_type":"image/jpeg",
                        "data":base64_image
                    },
                },
                {
                    "type":"text",
                    "text":"What is happening in this picture?"
                }
            ]
        }
    ]
}

payload_sample={
  "modelId": "anthropic.claude-3-5-haiku-20241022-v1:0",
  "contentType": "application/json",
  "accept": "application/json",
  "body": {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 200,
    "top_k": 250,
    "stopSequences": [],
    "temperature": 1,
    "top_p": 0.999,
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "hello world"
          }
        ]
      }
    ]
  }
}


bedrock_runtime_client=boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)


response=bedrock_runtime_client.invoke_model(
    modelId=model_id,
    body=json.dumps(payload_sample),
    accept="application/json",
    contentType="application/json",
)

print(response.get('body').read())
