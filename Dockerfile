# syntax=docker/dockerfile:1.2
FROM python:3.8

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run api.py when the container launches
CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "80"]
