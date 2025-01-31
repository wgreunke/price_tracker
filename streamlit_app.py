#This is a streamlit app that will allow the user to view the price tracker data.
import streamlit as st
import pandas as pd
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt


#When running streamlit, use this in the command to get boto3 to work
# C:/Python312/python.exe -m      streamlit run c:/Users/kahin/Documents/Python/price_tracker/streamlit_app.py


#Notes:
#Need to fix the datae time so that it is in pacific time.
#You are fetching all the images from the S3 bucket, even if they are not in the filtered data.  Need to improve this.



load_dotenv()

aws_access_key_id = os.getenv('aws_access_key_id')
aws_secret_access_key = os.getenv('aws_secret_access_key')



#Load the price tracker data from DynamoDB
dynamodb_connection = boto3.client('dynamodb', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)


#Get all the items from the table
dyanamo_response = dynamodb_connection.scan(TableName='price_tracker')
# Remove the 'S' and 'N' prefixes from the cell values
dyanamo_response['Items'] = [
    {k: (v['S'] if 'S' in v else v.get('N', None)) for k, v in item.items()} 
    for item in dyanamo_response['Items']
]

#Convert the response to a pandas dataframe
price_tracker_data = pd.DataFrame(dyanamo_response['Items'])

#Create a max price from the entire data set
price_tracker_data['list_price'] = price_tracker_data['list_price'].astype(float)
max_price = float( price_tracker_data['list_price'].max())


#Convert Unix timestamp to datetime only showing year month and day
price_tracker_data['year_month_day'] = pd.to_datetime(price_tracker_data['pacific_datetime'], unit='s').dt.date

#Order the data by the year_month_day column descending
price_tracker_data = price_tracker_data.sort_values(by='year_month_day', ascending=False)

#put the datetime column in the first position
price_tracker_data = price_tracker_data[['year_month_day','pacific_datetime', 'product', 'channel', 'list_price', 'sale_amount', 'sale_price', 'url', 'image_name']]

#Sort the data by the pacific_datetime2 column
price_tracker_data = price_tracker_data.sort_values(by='pacific_datetime')



#Generate a list of all the products and then show a table that has the lattest sales price and list price for each product
#Sort by product name
#Show the url for the product.  Also in the table, make the url a clickable link.
products_overview = price_tracker_data[['product', 'sale_price', 'list_price', 'sale_amount', 'url']].drop_duplicates(subset='product')
products_overview = products_overview.sort_values(by='product')
st.write("Products Overview")
# Show the products overview with clickable links for URLs
products_overview['url'] = products_overview['url'].apply(lambda x: f'<a href="{x}" target="_blank">Go to Site</a>')

# Add CSS to center and bold the header
styled_table = products_overview.to_html(escape=False)
styled_table = styled_table.replace('<thead>', '<thead style="font-weight: bold; text-align: center;">')
styled_table = styled_table.replace('<table>', '<table style="margin-left: auto; margin-right: auto;">')

st.markdown(styled_table, unsafe_allow_html=True)  # Display the table with clickable links




# Add ability to filter by product name (update the column name to match your actual data)
# You'll need to replace 'product_name' with the actual column name from your CSV
product_name = st.selectbox('Select a product', sorted(price_tracker_data['product'].unique()))  # assuming the column is called 'name'
#sort product_name by the product column


filtered_data = price_tracker_data[price_tracker_data['product'] == product_name]  # make sure to use the same column name here

#order the filtered data by the pacific_datetime column descending
filtered_data = filtered_data.sort_values(by='pacific_datetime', ascending=False)

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
#Show the x axis as a year month day


plt.plot(filtered_data['year_month_day'], filtered_data['sale_price'], label='Sale Price')
plt.plot(filtered_data['year_month_day'], filtered_data['list_price'], label='List Price')


# Customize plot
plt.title('Sale Price and List Price Over Time')
plt.xlabel('Date')
plt.ylabel('Price')
plt.ylim(0, max_price + 100)  # Add some padding
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
