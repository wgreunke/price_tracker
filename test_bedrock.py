import boto3
import json
model_id = "amazon.nova-pro-v1:0"

bedrock_client = boto3.client(service_name='bedrock-runtime', region_name='us-east-1') 
model_id = 'anthropic.claude-v2'  # Replace with the desired model ID

prompt3="""This is a picture of a product from a website.  Tell me the:
<model_number>
<product_name>
<product_description>
<list_price>
<sale_amount>
"""

# Option 1: Using raw string (recommended)
image_path = r"C:\Users\kahin\Downloads\16-af0075cl_1735282644.png"



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
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 200,
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ]
}

response = bedrock_client.invoke_model(
    modelId=model_id,
    body=json.dumps(payload)
)

result = json.loads(response['body'].read())
generated_text = result['content'][0]['text']  # Updated to match Claude's response format
print(f"Response: {generated_text}")