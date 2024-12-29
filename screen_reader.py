#This app takes loads a url and then takes a screenshot.
#The screenshot is then saved to an image file and uplaoded to s3
#The screeshot uses the bash shell to launch a react browser, wait some time and then takes a screenshot.

import boto3
import os
import time
import subprocess
import pyautogui


print("Starting the screen reader")
print("Connecting to DynamoDB")

#Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
table = dynamodb.Table('products')
#Connect to S3
s3=boto3.client('s3',region_name='us-west-1')




#Scan the table to get all items
response = table.scan()
products = response['Items']
print(f"Initial scan found {len(products)} items")  # Debug print

#If there are more items (pagination), keep scanning
while 'LastEvaluatedKey' in response:
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    products.extend(response['Items'])

# Moved the printing loop outside of the while loop
print("\nPrinting all products:")  # Debug print

# *************** Main loop ***************

for product in products:
    temp_product_name = product['product_name']
    temp_url = product['url']
    
    # Add timestamp to filename to make it unique
    timestamp = int(time.time())
    unique_filename = f"{temp_product_name}_{timestamp}"
    
    # Fix string syntax for the command
    command = f'start msedge "{temp_url}"'
    
    subprocess.run(command, shell=True)
    time.sleep(5)
    
    try:
        screenshot = pyautogui.screenshot()
        print(f"Taking screenshot for {temp_product_name}")
        
        # Use unique filename for both local and S3 storage
        local_path = f"C:/Users/kahin/Downloads/{unique_filename}.png"
        screenshot.save(local_path)
        
        # Upload to S3 with unique filename
        s3.upload_file(local_path, 'vendor-images-storage', f"{unique_filename}.png")
        
        # Clean up local file
        os.remove(local_path)
        
    except Exception as e:
        print(f"Error processing {temp_product_name}: {str(e)}")




