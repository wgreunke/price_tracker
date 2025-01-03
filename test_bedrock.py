import boto3
import json
import base64


#Code examples, each model has a differnt syntax.
#https://docs.aws.amazon.com/code-library/latest/ug/python_3_bedrock-runtime_code_examples.html
bedrock_client = boto3.client(service_name='bedrock-runtime', region_name='us-east-1') 
#model_id = 'anthropic.claude-v2'  # Replace with the desired model ID

prompt3="""This is a picture of a product from a website.  Tell me the:
<model_number>
<product_name>
<product_description>
<list_price>
<sale_amount>
"""

# Load the image and convert to base64
#image_path = r"C:\Users\kahin\Downloads\16-af0075cl_1735282644.png"
image_path = r"C:/Users/kahin/Downloads/16-af0075cl_1735282644.png"

with open(image_path,"rb") as image_file:
    base64_image=base64.b64encode(image_file.read()).decode('utf-8')


#pass the image to the llm along with the prompt
prompt4=f"""This is a picture of a product from a website.  Tell me the:
<model_number>
<product_name>
<product_description>
<list_price>
<sale_amount>
{image_path}""" 

prompt2="Tell me what this picture is about:"
prompt = "Tell me a joke"

payload = {
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "text": "Tell me a new joke",
                    "image": base64_image,
                }
            ]
        }
    ],
    "inferenceConfig": {
        "max_new_tokens": 1000
    }
}


response = bedrock_client.invoke_model(
    modelId="amazon.nova-pro-v1:0",
    body=json.dumps(payload)
)

result = json.loads(response['body'].read())
#generated_text = result['outputs'][0]['text']  # Nova-Pro uses 'outputs' instead of 'content'

#Full dump of the response
print("Response Structure:", json.dumps(result, indent=2))

#print(f"Response: {generated_text}")