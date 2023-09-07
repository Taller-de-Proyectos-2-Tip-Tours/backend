# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code into the container
COPY . /app

# Define environment variable
ENV NAME TipTours

# Expose the port your Flask app will run on
EXPOSE 5000

# Run your Python application
CMD ["python3", "main.py"]