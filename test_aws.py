import boto3

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='us-west-1')

# List tables
response = dynamodb.list_tables()

# Print table names
table_names = response.get('TableNames', [])
if not table_names:
    print("No tables found in the specified region.")
else:
    print("Tables in the specified region:")
    for table_name in table_names:
        print(f" - {table_name}")


import boto3


# Reference the products table
table = dynamodb.Table('products')

# Scan the table and fetch all items
response = table.scan()

# Print the items
items = response.get('Items', [])
if not items:
    print("No data found in the products table.")
else:
    print("Data from the products table:")
    for item in items:
        print(item)
