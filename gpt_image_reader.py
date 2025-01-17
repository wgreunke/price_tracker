#From https://platform.openai.com/docs/guides/vision/overview
#This sends an image to chat gpt and asks it to describe the image. 
import openai
import base64
from openai import OpenAI
import os
from dotenv import load_dotenv
import xml.etree.ElementTree as ET


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



#With xml
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text":(
                      "This is a screenshot of a computer for sale. "
                        "Please extract the following details: <model_number>, <list_price>, <sale_price>, <sale_amount>. "
                        "Format the response as XML in the following structure:\n\n"
                        "<details>\n"
                        "  <model_number>...</model_number>\n"
                        "  <list_price>...</list_price>\n"
                        "  <sale_price>...</sale_price>\n"
                        "  <sale_amount>...</sale_amount>\n"
                        "</details>"
                    ),
                    
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        }
    ],
)



#print(response.choices[0])



#Once you have the responce, strip out the values and convert them to decimals.
response_choice=response.choices[0]
#print(response_choice)


# Simulating the response content
xml_data = response_choice.message.content

#This function takes a currency value and converts it to decimal.
#Strip out dollar sign and convert to float
def convert_currency_to_decimal(dollar_amount):
  no_dollar_sign=dollar_amount.replace('$', '')
  no_comma=no_dollar_sign.replace(',', '')
  return float(no_comma)



# Strip Markdown code block delimiters if present
if xml_data.startswith("```xml") and xml_data.endswith("```"):
    xml_data = xml_data[6:-3].strip()  # Remove '```xml' at the start and '```' at the end

try:
    # Parse the XML data
    root = ET.fromstring(xml_data)

    # Extract data from the XML
    model_number = root.find("model_number").text
    list_price = convert_currency_to_decimal(root.find("list_price").text)
    sale_price = convert_currency_to_decimal(root.find("sale_price").text)
    sale_amount = convert_currency_to_decimal(root.find("sale_amount").text)

  
except ET.ParseError as e:
    print(f"Error parsing XML: {e}")



#This function takes in an image, sends it to chat gpt, and returns the extracted data as a dictionary. 
def get_price_data_from_openai(local_path):
    base64_image = encode_image(local_path)

    #Send the image to chat gpt and get the response
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text":(
                          "This is a screenshot of a computer for sale. "
                            "Please extract the following details: <model_number>, <list_price>, <sale_price>, <sale_amount>. "
                            "Format the response as XML in the following structure:\n\n"
                            "<details>\n"
                            "  <model_number>...</model_number>\n"
                            "  <list_price>...</list_price>\n"
                            "  <sale_price>...</sale_price>\n"
                            "  <sale_amount>...</sale_amount>\n"
                            "</details>"
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
    )
    
    #Call the model
    xml_data = response.choices[0].message.content
    
    # Strip Markdown code block delimiters if present
    if xml_data.startswith("```xml") and xml_data.endswith("```"):
        xml_data = xml_data[6:-3].strip()  # Remove '```xml' at the start and '```' at the end

    try:
        # Parse the XML data
        root = ET.fromstring(xml_data)

        # Extract data from the XML
        model_number = root.find("model_number").text
        list_price = convert_currency_to_decimal(root.find("list_price").text)
        sale_price = convert_currency_to_decimal(root.find("sale_price").text)
        sale_amount = convert_currency_to_decimal(root.find("sale_amount").text)

        
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")

    return model_number, list_price, sale_price, sale_amount



#******************** Main ***********************
#This is the code to run for testing when run directly.
def main(): 
    print("This code is only executed when the file is run directly.") 
    #Testing
    print("Testing Results")
    local_path="16-af0075cl_1735282644.png"
    model_number, list_price, sale_price, sale_amount = get_price_data_from_openai(local_path)
    print(f"Model Number: {model_number}")
    print(f"List Price: {list_price}")
    print(f"Sale Price: {sale_price}")
    print(f"Sale Amount: {sale_amount}")
    
if __name__ == "__main__": main()