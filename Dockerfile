# Use official Python image
FROM python:3.10-slim

WORKDIR /app

COPY . /app

# Install dependencies
RUN pip install --no-cache-dir flask pytest

# Default command (can be overridden)
CMD ["python", "app.py"]
