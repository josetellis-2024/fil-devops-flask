# Use an official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the project files
COPY . .

# Expose the Flask port
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
