# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# --- EXPLICIT COPY ---
# We will copy the requirements file first, by itself.
# This is a best practice that improves Docker's caching.
# The path is now relative to the Dockerfile's location.
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Now, copy the rest of the application's code.
# The '.' refers to the location of the Dockerfile (the 'backend' dir).
COPY . .

# Install system dependencies (moved after pip install to improve caching)
# We only need to run this if the code copy step changes.
# PyMuPDF might need some of these.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run your app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]