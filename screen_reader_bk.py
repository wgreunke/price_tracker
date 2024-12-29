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
    #print(f"Product: {product['product_name']} - URL: {product['url']}")
    print(product)
    #Take a screenshot of the url
    command = f'start msedge {product['url']}'

    # Execute the command
subprocess.run(command, shell=True)

    #wait 3 seconds after loading page to be sure all images are pulled in.
time.sleep(3)    

    # Take the screenshot
screenshot = pyautogui.screenshot()
print("taking shot now")

    # Save the screenshot
    #screenshot.save("screenshot.png")
    screenshot.save(f"C:/Users/kahin/Downloads/{temp_product_name}.png")
    #Now save the screenshot to s3
    s3.upload_file(f"C:/Users/kahin/Downloads/{temp_product_name}.png", 'kahin-test-bucket', f"{temp_product_name}.png")



#temp_url = "www.google.com"
#temp_product_name = "16-af0075cl"
#print(temp_url)


