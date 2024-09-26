# Use Python image as the base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code into the container
COPY . .

# Expose the port the application runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "app.py"]  # Adjust this command to match your application's entry point
