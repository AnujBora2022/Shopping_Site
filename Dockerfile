FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install pip dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Specify the command to run your app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
