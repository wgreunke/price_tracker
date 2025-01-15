#This is the main program that will be used to load model numbers, load images, send to the model, and get the results.
from s3_tools import get_list_of_images
from dynamo_tools import take_screenshot
from dynamo_tools import upload_screenshot_to_s3
from dynamo_tools import write_new_record_to_price_tracker
from dynamo_tools import get_list_of_products


#Fetch the list of products and vendors from DynamoDB
products = get_list_of_products()
print("List of products:" )
for product in products:
    print(product['product_name'])
    print(product['url'])
    print(product['channel'])

    #For each product, load the url and take a screenshot of the page.
    timestamp,temp_image_name, temp_image = take_screenshot(product['product_name'], product['url'], product['channel'])

    #Save the screenshot to S3
    upload_screenshot_to_s3(temp_image_name, temp_image)

    #Get the price data from openai
    #Use dummy values for now
    list_price = 800
    sale_amount = 200
    sale_price = 100

    #Write a new record to the DynamoDB table with the timestamp, product name, and product url.
    write_new_record_to_price_tracker(
        timestamp=timestamp, 
        product_name=product['product_name'], 
        channel=product['channel'], 
        image_name=temp_image_name, 
        list_price=list_price, 
        sale_amount=sale_amount, 
        sale_price=sale_price, 
        url=product['url']
    )


#Save the screenshot to S3
print("Testing the S3 connection by listing the images")
images = get_list_of_images()
for image_item in images:
    #The images items have the format: s3.ObjectSummary(bucket_name='vendor-images-storage', key='16-af0075cl_1735282644.png')
    #You just need the key.
    print(image_item.key)  # Will print just the filename/key



#Send the screenshot to the model

#Get the results from the model

#Send the results to DynamoDB

