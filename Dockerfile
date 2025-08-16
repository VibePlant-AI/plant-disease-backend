# Dockerfile (in plant-disease-backend repo)
FROM python:3.13-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install uv, the fast package manager
RUN pip install uv

# Copy only the files needed for dependency installation
COPY pyproject.toml uv.lock ./

# Use uv to sync the environment from the lock file (fast and reproducible)
RUN uv pip sync uv.lock

# Copy the rest of the Django application code
COPY . .

# Run database migrations during the build process
# This ensures the database is ready when the container starts
RUN python manage.py migrate

# Expose the port Gunicorn will run on
EXPOSE 8000

# The command to start the Gunicorn production server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]