###########################
# backend/Dockerfile
###########################
FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED=1

# ─── system deps (WeasyPrint itd.) ───
RUN apt-get update && apt-get install -y --no-install-recommends \
      libcairo2 libpangocairo-1.0-0 libpangoft2-1.0-0 \
      libgdk-pixbuf2.0-0 libffi-dev fonts-liberation shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ─── Python deps ───
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ─── kod źródłowy ───
COPY . .

# ─── jeden, OSTATECZNY CMD ───
CMD ["sh","-c","alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]
