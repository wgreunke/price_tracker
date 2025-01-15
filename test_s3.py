import boto3
from boto3.session import Session


s4=boto3.client('s3',region_name='us-west-1')

# Create a session with your credentials from cli
session = Session(
    region_name='us-west-1'
)

# Create S3 client using the session
s3 = session.resource('s3')
print('Accessing bucket')
bucket = s3.Bucket("vendor-images-storage")


temp_product_name = "16-af0075cl"

#Get a list of files in the bucket to make sure connection is working
for item in bucket.objects.all():
    print(item.key)

"""
s4.upload_file(
    f"C:/Users/kahin/Downloads/{temp_product_name}.png", 
    'vendor-images-storage', 
    f"{temp_product_name}.png"
)
"""
#print(s4.list_objects_v2(Bucket='vendor-images-storage'))

#Get a list of files in the bucket to make sure connection is working
for item in bucket.objects.all():
    print(item.key)



