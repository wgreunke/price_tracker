#Having problems with the image.
#First it asks for a toolType, then when I include that it says that source is not a valid type.  
# Going to try using gpt to get things going. 
 

# Use the native inference API to send a text message to Amazon Titan Text.

import boto3
import json
import base64
from botocore.exceptions import ClientError

# Create a Bedrock Runtime client in the AWS Region of your choice.
client = boto3.client("bedrock-runtime", region_name="us-east-1")

#The titan model and the noval model have different request structure.


#Load and convert the image
image_path = "C:/Users/kahin/Downloads/16-af0075cl_1735282644.png"
with open(image_path, 'rb') as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()




# Set the model ID, e.g., Titan Text Premier.
model_id="amazon.nova-pro-v1:0" 

# Define the prompt for the model.
prompt = "Describe the purpose of a 'hello world' program in one line."

# Format the request payload using the model's native structure.
#Copoied from model playground.
request={"messages":
         [
         {"role":"user","content":
          [
              {"text":"tell me a joke"},
              {"type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": encoded_image
                    }
                },
          ]
         }
],
"inferenceConfig":{"maxTokens":512,"stopSequences":[],"temperature":0.7,"topP":0.9}}
 

request = {
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "text": "Tell me a joke",
            
                },
                {
                    "type": "image",
                    "toolUse": "none",  # Add toolUse for image content
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": encoded_image
                    }
                }
            ]
        }
    ],
    "inferenceConfig": {
        "maxTokens": 512,
        "stopSequences": [],
        "temperature": 0.7,
        "topP": 0.9
    }
}


# Convert the native request to JSON.
#request = json.dumps(titan_request)
request = json.dumps(request)

try:
    # Invoke the model with the request.
    response = client.invoke_model(modelId=model_id, body=request)

except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)

# Decode the response body.
model_response = json.loads(response["body"].read())

# Extract and print the response text.
#response_text = model_response["results"][0]["outputText"]
print("")
print("--------------------------------")


print(model_response)


