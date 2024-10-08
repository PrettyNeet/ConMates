# Use official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app's source code
COPY . .

# Set environment variables
ENV BOT_TOKEN=${BOT_TOKEN}

# Run the application
CMD ["python", "bot.py"]
