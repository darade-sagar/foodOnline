FROM python:3.10.1

# Install required packages
RUN pip install -r requirements.txt

# Set the working directory
WORKDIR /app

# Copy the application code to the container
COPY . /app

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
