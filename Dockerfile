FROM python:3.13-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Upgrade pip & tools
RUN pip install --upgrade pip setuptools wheel

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies
RUN pip install .

# Copy the rest of the Django application code
COPY . .

# Expose the port Gunicorn will run on
EXPOSE 8000

# Run migrations + start Gunicorn when the container starts
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 backend.wsgi:application"]
