#This is the main program that will be used to load model numbers, load images, send to the model, and get the results.
from s3_tools import get_list_of_images
from dynamo_tools import get_list_of_products

#Load the list of products and vendors from DynamoDB
products = get_list_of_products()
print("List of products:" )
for product in products:
    print(product['product_name'])

#For each product, load the url and take a screenshot of the page.

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

