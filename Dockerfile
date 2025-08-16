# Dockerfile (in plant-disease-backend repo)
FROM python:3.13-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install pip-tools to support pyproject.toml directly (optional, safer)
RUN pip install --upgrade pip setuptools wheel

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies from pyproject.toml
# This installs the project and its dependencies
RUN pip install .

# Copy the rest of the Django application code
COPY . .

# Run database migrations during the build process
RUN python manage.py migrate

# Expose the port Gunicorn will run on
EXPOSE 8000

# The command to start the Gunicorn production server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]
