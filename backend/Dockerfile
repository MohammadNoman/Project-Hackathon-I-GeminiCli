# Use a Python base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Explicitly add site-packages to PYTHONPATH
ENV PYTHONPATH=/usr/local/lib/python3.9/site-packages:$PYTHONPATH

# Set PYTHONPATH to include the working directory
ENV PYTHONPATH /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip show python-json-logger
RUN python -c "import sys; print(sys.path)"

# Copy the entire backend application code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
# Assuming the main application object is 'app' in 'src.main'
CMD python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
