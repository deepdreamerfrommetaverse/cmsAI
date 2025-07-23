# Stage 1: Build frontend
FROM node:18 AS frontend-build
WORKDIR /app
COPY frontend/package*.json ./frontend/
RUN npm install -prefix frontend
COPY frontend/. ./frontend/
RUN npm run --prefix frontend build

# Stage 2: Build backend image
FROM python:3.11-slim-bullseye AS backend
# Install system dependencies for WeasyPrint (for PDF generation) and others
RUN apt-get update && apt-get install -y --no-install-recommends \
    libcairo2 libpangocairo-1.0-0 libpangoft2-1.0-0 \
    libgdk-pixbuf2.0-0 libffi-dev shared-mime-info fonts-liberation && \
    rm -rf /var/lib/apt/lists/*
# Set working directory
WORKDIR /app
# Copy backend code
COPY backend ./backend
COPY alembic ./alembic
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Copy frontend build output to be served (if backend were to serve static)
COPY --from=frontend-build /app/frontend/dist ./frontend_dist
# Expose port
EXPOSE 8000
# Default command to run the API server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
