#This is a streamlit app that will allow the user to view the price tracker data.
import streamlit as st
import pandas as pd
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import os
from dotenv import load_dotenv

#When running streamlit, use this in the command to get boto3 to work
# C:/Python312/python.exe -m      streamlit run c:/Users/kahin/Documents/Python/price_tracker/streamlit_app.py  
load_dotenv()

aws_access_key_id = os.getenv('aws_access_key_id')
aws_secret_access_key = os.getenv('aws_secret_access_key')

#Connect to the S3 bucket
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)   
#Get a list of all the files in the S3 bucket
s3_objects = s3.list_objects_v2(Bucket='vendor-images-storage')  
st.write(s3_objects)


#Show this image from the S3 bucket 1737154609_17-cn4065cl_Costco.png
image_key = '1737154609_17-cn4065cl_Costco.png'
image_url = s3.generate_presigned_url('get_object', Params={'Bucket': 'vendor-images-storage', 'Key': image_key}, ExpiresIn=3600)
st.image(image_url)



#Load the price tracker data from csv
price_tracker_data = pd.read_csv('results.csv')

#Convert Unix timestamp to datetime only showing year month and day
price_tracker_data['pacific_datetime2'] = pd.to_datetime(price_tracker_data['pacific_datetime'], unit='s').dt.date

#put the datetime column in the first position
price_tracker_data = price_tracker_data[['pacific_datetime2', 'product', 'channel', 'list_price', 'sale_amount', 'sale_price', 'url']]

#Sort the data by the pacific_datetime2 column
price_tracker_data = price_tracker_data.sort_values(by='pacific_datetime2')

# Print column names to see what's available
st.write("Available columns:", price_tracker_data.columns)

# Add ability to filter by product name (update the column name to match your actual data)
# You'll need to replace 'product_name' with the actual column name from your CSV
product_name = st.selectbox('Select a product', price_tracker_data['product'].unique())  # assuming the column is called 'name'

#Createa list of the unique names from the product column   
product_names = price_tracker_data['product'].unique()



filtered_data = price_tracker_data[price_tracker_data['product'] == product_name]  # make sure to use the same column name here

#Display the filtered price tracker data
st.write(filtered_data)

#Create a line chart of the sale price plotted against the date
st.line_chart(filtered_data.set_index('pacific_datetime2')['sale_price'])  # Set the index to the date column

