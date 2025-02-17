# Use an official Python runtime as a parent image
FROM python

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/

# Install any dependencies in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port the app runs on (default Django port is 8000)
EXPOSE 8000

# Run Django migrations and start the app
CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
