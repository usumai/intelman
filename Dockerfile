# Use the official Python slim image as the base image
FROM python:3.9-slim

# Set a label for the image (optional)
LABEL maintainer="your_email@example.com" \
      app="intelman"

# Set the working directory inside the container
WORKDIR /app

# Copy the dependency file and install required packages
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port that the Flask app runs on
EXPOSE 5000

# Set the default command to run your Flask app from the app folder
CMD ["python", "app/app.py"]
