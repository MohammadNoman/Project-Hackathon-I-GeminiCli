# Use a Python base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy the entire backend application code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
CMD python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
