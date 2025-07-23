# Use a slim Python image as base
FROM python:3.11-slim-bullseye

# Environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies for WeasyPrint and others
RUN apt-get update && apt-get install -y --no-install-recommends \
    libcairo2 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir fastapi uvicorn[standard] sqlalchemy alembic passlib[bcrypt] pyjwt openai stripe tweepy requests weasyprint

# Set working directory
WORKDIR /app

# Copy project code
COPY . /app

# Expose port 8000 for the API
EXPOSE 8000

# Default command to run the API server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
