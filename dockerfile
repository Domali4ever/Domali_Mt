# Use Python 3.10 as base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /usr/src/app

# Install Cassandra Python driver and Pandas
RUN pip install pandas cassandra-driver openpyxl

# Copy the local Python script and Excel file into the container
COPY insert_to_cassandra.py .
COPY mass_email_campaign_updated.xlsm .

# Run the Python script when the container starts
CMD ["python", "./insert_to_cassandra.py"]
