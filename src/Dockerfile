# Base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . .

# Expose port 8080
EXPOSE 8080

# Define the entry point to run the Flask app
CMD ["python", "main.py"]
