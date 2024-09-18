import pandas as pd
from cassandra.cluster import Cluster
import asyncio

# File path for your CSV file
file_path = r"C:\Users\Domali\Documents\DOMALI_Mt\mass_email_campaign_updated_utf8.csv" 

# Connect to Cassandra
cluster = Cluster(['127.0.0.1'])  
session = cluster.connect('domali_cass') 

# Function to insert data into Cassandra
async def insert_data_into_cassandra():
    try:
        # Read CSV file
        df = pd.read_csv(file_path)

        # Strip whitespace from the column names and convert to lower case
        df.columns = df.columns.str.strip().str.lower()

        # Print the column names to check their exact format
        print("Columns in the DataFrame:")
        print(df.columns.tolist())

        # Debugging: Print the first few rows of the DataFrame
        print("First few rows of the DataFrame:")
        print(df.head())

        # Check if 'status' column exists
        if 'status' not in df.columns:
            print("Error: 'status' column not found in DataFrame.")
            return

        # Iterate through rows in the DataFrame
        for index, row in df.iterrows():
            # Prepare CQL statement for inserting data into the email_campaign_domali table
            query = """
            INSERT INTO email_campaign_domali (status, last_email_sent, first_name, last_name, email, 
            direct_phone, mobile, company, title, website, 
            street_address, city, state, zip, 
            country, start_date, level, function) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Execute the query with error handling
            try:
                session.execute(query, (
                    row['status'], 
                    row['last_email_sent'], 
                    row['first_name'], 
                    row['last_name'], 
                    row['email'], 
                    row['direct_phone'], 
                    row['mobile'],
                    row['company'], 
                    row['title'], 
                    row['website'], 
                    row['street_address'], 
                    row['city'], 
                    row['state'], 
                    row['zip'], 
                    row['country'], 
                    row['start_date'], 
                    row['level'], 
                    row['function']
                ))
                print(f"Inserted row {index + 1}")
            except Exception as e:
                print(f"Error inserting row {index + 1}: {e}")

    except Exception as e:
        print(f"Error reading the CSV or connecting to Cassandra: {e}")

# Running the async function
asyncio.run(insert_data_into_cassandra())
