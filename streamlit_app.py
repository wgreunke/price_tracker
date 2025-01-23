#This is a streamlit app that will allow the user to view the price tracker data.
import streamlit as st
import pandas as pd
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt




#Notes:
#Need to fix the datae time so that it is in pacific time.
#You are fetching all the images from the S3 bucket, even if they are not in the filtered data.  Need to improve this.




#When running streamlit, use this in the command to get boto3 to work
# C:/Python312/python.exe -m      streamlit run c:/Users/kahin/Documents/Python/price_tracker/streamlit_app.py  
load_dotenv()

aws_access_key_id = os.getenv('aws_access_key_id')
aws_secret_access_key = os.getenv('aws_secret_access_key')



#Load the price tracker data from DynamoDB
dynamodb_connection = boto3.client('dynamodb', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)


#Get all the items from the table
dyanamo_response = dynamodb_connection.scan(TableName='price_tracker')
# Remove the 'S' and 'N' prefixes from the cell values
dyanamo_response['Items'] = [
    {k: (v['S'] if 'S' in v else v['N']) for k, v in item.items()} 
    for item in dyanamo_response['Items']
]

#Convert the response to a pandas dataframe
price_tracker_data = pd.DataFrame(dyanamo_response['Items'])



#Convert Unix timestamp to datetime only showing year month and day
price_tracker_data['year_month_day'] = pd.to_datetime(price_tracker_data['pacific_datetime'], unit='s').dt.date

#put the datetime column in the first position
price_tracker_data = price_tracker_data[['year_month_day','pacific_datetime', 'product', 'channel', 'list_price', 'sale_amount', 'sale_price', 'url', 'image_name']]

#Sort the data by the pacific_datetime2 column
price_tracker_data = price_tracker_data.sort_values(by='pacific_datetime')

#st.write("modified table")
#st.write(price_tracker_data)


# Add ability to filter by product name (update the column name to match your actual data)
# You'll need to replace 'product_name' with the actual column name from your CSV
product_name = st.selectbox('Select a product', price_tracker_data['product'].unique())  # assuming the column is called 'name'




filtered_data = price_tracker_data[price_tracker_data['product'] == product_name]  # make sure to use the same column name here

#Display the filtered price tracker data
st.write("Filtered Data")
st.write(filtered_data)

#make pacific_datetime an integer
filtered_data['pacific_datetime'] = filtered_data['pacific_datetime'].astype(int)
#make sale_price an integer
filtered_data['sale_price'] = filtered_data['sale_price'].astype(float)
#make list_price an integer
filtered_data['list_price'] = filtered_data['list_price'].astype(float)


plt.figure(figsize=(10, 6))

# Plot lines
plt.plot(filtered_data['pacific_datetime'], filtered_data['sale_price'], label='Sale Price')
plt.plot(filtered_data['pacific_datetime'], filtered_data['list_price'], label='List Price')


# Customize plot
plt.title('Sale Price and List Price Over Time')
plt.xlabel('Date')
plt.ylabel('Price')
plt.ylim(0, filtered_data['sale_price'].max() + 10)  # Add some padding
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Display in Streamlit
st.pyplot(plt)



#************************ Handle Images *****************************
#Connect to the S3 bucket
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)   
#Get a list of all the files in the S3 bucket
s3_objects = s3.list_objects_v2(Bucket='vendor-images-storage')  
#st.write(s3_objects)




#Pull the images from the S3 bucket
for index, row in filtered_data.iterrows():
    # Check if 'image_key' exists in the row
    print(row['image_name'])
    if 'image_name' in row:
        image_name = row['image_name']
        image_url = s3.generate_presigned_url('get_object', Params={'Bucket': 'vendor-images-storage', 'Key': image_name}, ExpiresIn=3600)
        st.write(image_name)
        st.write(row['year_month_day'])
        st.image(image_url)
    else:
        st.warning(f"No image key found for index {index}.")  # Notify if the key is missing


#Show this image from the S3 bucket 1737154609_17-cn4065cl_Costco.png
#image_key = '1737154609_17-cn4065cl_Costco.png'
#image_url = s3.generate_presigned_url('get_object', Params={'Bucket': 'vendor-images-storage', 'Key': image_key}, ExpiresIn=3600)
#st.image(image_url)



# Print column names to see what's available
#st.write("Available columns:", price_tracker_data.columns)
