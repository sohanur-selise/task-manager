# Use the official Python base image with Python 3.8
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the Pipfiles to the container
COPY Pipfile Pipfile.lock /app/

# Install dependencies using pipenv
RUN pip install pipenv
RUN pipenv install --deploy --system

RUN pipenv install django

# Copy the Django project to the container
COPY ./taskmanager /app/taskmanager

# Expose the application's port (adjust if needed)
EXPOSE 8000

# Run the Django development server
CMD ["pipenv", "run", "python", "taskmanager/manage.py", "runserver", "0.0.0.0:8000"]
