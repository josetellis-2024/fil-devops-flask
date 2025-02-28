FROM python:3.10-slim

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app    

# Copy and install dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy application files
COPY . .

# Expose the Flask default port
EXPOSE 5000

# Command to run the Flask app
CMD ["python3", "-m", "flask", "run","--host=0.0.0.0"]