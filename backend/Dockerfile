# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install production dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . /app

# Expose the port on which the FastAPI application will run
EXPOSE 7860

# Command to run the application using Uvicorn
# Assuming your main FastAPI application instance is in backend/src/main.py and named 'app'
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]
