#This is a streamlit app that will allow the user to view the price tracker data.

import streamlit as st
import pandas as pd
#Load the price tracker data from csv
price_tracker_data = pd.read_csv('sample_price_tracker.csv')

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


