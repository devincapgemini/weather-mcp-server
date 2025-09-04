# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose a default port
EXPOSE 8000

# Run the application, using the PORT variable provided by the cloud environment
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
