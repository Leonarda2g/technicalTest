# Use the official Python image from Docker Hub
FROM python:3.9

# Set the working directory
WORKDIR /techTest

# Copy the requirements file into the container at /techTest
COPY requirements.txt /techTest/

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /techTest/

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
