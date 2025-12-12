# Use the official Python image as a base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Debug step: Show the contents of requirements.txt
RUN cat requirements.txt

# Install build tools for Python dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    rustc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Debug step: Show Python version and pip version
RUN python --version && pip --version

# Debug step: Attempt to install dependencies one by one
RUN pip install --no-cache-dir aiogram==3.22.0
RUN pip install --no-cache-dir dotenv==0.9.9
RUN pip install --no-cache-dir mistralai==1.9.11
RUN pip install --no-cache-dir pydantic==2.11.10
RUN pip install --no-cache-dir pydantic-settings==2.12.0
RUN pip install --no-cache-dir python-dateutil==2.9.0.post0
RUN pip install --no-cache-dir python-dotenv==1.2.1
RUN pip install --no-cache-dir PyYAML==6.0.3
RUN pip install --no-cache-dir yarl==1.22.0

# Copy the rest of the application code into the container
COPY . .

# Expose the port the bot will run on (if applicable)
EXPOSE 8080

# Set the command to run the bot
CMD ["python", "app.py"]