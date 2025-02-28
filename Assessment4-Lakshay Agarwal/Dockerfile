# Use official Python image as base
FROM python:3.13

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port for Flask
EXPOSE 5000

# Run Flask application
CMD ["python", "app.py"]
