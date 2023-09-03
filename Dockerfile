# Use the official Python image as a base image
FROM python:3.10.0

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable for the FastAPI app
ENV APP_MODULE="main:app"

# Run the app
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "80", "--reload", "main:app"]