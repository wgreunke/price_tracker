#This was copied from the screen_reader.py file.
#This app takes loads a url and then takes a screenshot.
#The screenshot is then saved to an image file and uplaoded to s3
#The screeshot uses the bash shell to launch a react browser, wait some time and then takes a screenshot.

import boto3
import os
import time
import subprocess
import pyautogui
from datetime import datetime

#Tips on pulling screenshots.
#https://www.reddit.com/r/aws/comments/j4kmnq/how_do_i_get_graphics_output_from_my_ec2_instance/
#Python options: https://screenshotone.com/blog/how-to-take-website-screenshots-in-python/ Selenium, Pyppeteer, Playwright



#Connect to DynamoDB
print("Connecting to DynamoDB")
dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
table = dynamodb.Table('products')
price_tracker_table = dynamodb.Table('price_tracker')
#Connect to S3
s3=boto3.client('s3',region_name='us-west-1')

#Scan the table to get all items



# Moved the printing loop outside of the while loop
print("\nPrinting all products:")  # Debug print

# *************** Main loop ***************

#Given a list of products, take a screenshot of each product and save it to S3


def take_screenshot(product_name, product_url, product_channel):
    # Add timestamp to filename to make it unique
    #The timestamp is used as a unique id and will help searching the S3 bucket for the screenshot.
    timestamp = int(time.time())
    #add .png to the end of the filename
    unique_filename = f"{timestamp}_{product_name}_{product_channel}"
    
    # Fix string syntax for the command
    command = f'start msedge "{product_url}"'
    
    subprocess.run(command, shell=True)
    time.sleep(5)
    try:
        screenshot = pyautogui.screenshot()
        print(f"Taking screenshot for {product_name}")
        # Save screenshot to a temporary file
        local_path = f"C:/Users/kahin/Downloads/{unique_filename}.png"
        screenshot.save(local_path)
        return timestamp, unique_filename, local_path
    except Exception as e:
        print(f"Error processing {product_name}: {str(e)}")
        return None, None, None


#This takes the image and image name and uploads it to S3
def upload_screenshot_to_s3(temp_image_name, local_path):
    try:
        s3.upload_file(local_path, 'vendor-images-storage', f"{temp_image_name}.png")
      
    except Exception as e:
        print(f"Error uploading to S3: {str(e)}")



"""
#Old loop that is replicated in function above.
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

"""

def get_list_of_products():
    response = table.scan()
    return response['Items']


def write_new_record_to_price_tracker(timestamp, channel, image_name, list_price, product_name, sale_amount, sale_price, url):
    #Convert the timestamp to a string
    timestamp_str = str(timestamp)
    try:
        #Automatically get the date from the timestamp
        #Add .png to the end of the image_name
        image_name = f"{image_name}.png"
        date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        price_tracker_table.put_item(
            Item={
                'pacific_datetime': timestamp_str,
                'channel': channel,
                'image_name': image_name,
                'list_price': list_price,
                'product': product_name,
                'sale_amount': sale_amount,
                'sale_price': sale_price,
                'url': url,
                'date': date
            }
        )
        return True
    except Exception as e:
        print(f"Error writing to DynamoDB: {str(e)}")
        return False


#******************** Main ***********************
#This is the code to run for testing when run directly.
def main(): 
    print("This code is only executed when the file is run directly.") 
    #Testing
    print("")
    print("Starting Test")
    print("Getting list of products from DynamoDB")
    products = get_list_of_products()

    
    for product in products:
        print(product['product_name'])
        #Take a screenshot of the product
        timestamp,temp_image_name, temp_image = take_screenshot(product['product_name'], product['url'], product['channel'])
        #Upload the screenshot to S3
        upload_screenshot_to_s3(temp_image_name, temp_image)
        #Write a new record to the DynamoDB table
        sale_amount = 200
        sale_price = 100
        list_price = 800
        #Explicitly pass the values to the function
        write_new_record_to_price_tracker(
            timestamp= timestamp, 
            product_name=product['product_name'], 
            channel=product['channel'], 
            image_name=temp_image_name, 
            list_price=list_price, 
            sale_amount=sale_amount, 
            sale_price=sale_price, 
            url=product['url']
        )
     
        print("New record written to DynamoDB")


        
#Dummy values while waiting for the sale price and amount.
    timestamp = int(time.time())
    product_name = "Test Product"
    channel = "Test Channel"
    image_name = "Test Image"
    sale_amount = 200
    sale_price = 100
    list_price = 800
    url = "https://www.google.com"
    #write_new_record_to_dynamodb(timestamp, product_name, channel, image_name, list_price, sale_amount, sale_price, url)
        
if __name__ == "__main__": main()
