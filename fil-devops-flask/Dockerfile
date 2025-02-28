FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m appuser && \
    chown -R appuser:appuser /app
USER appuser

# Set environment variables
ENV FLASK_APP=app/__init__.py \
    FLASK_ENV=production \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Expose port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]