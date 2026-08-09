FROM python:3.12-slim

# Create a non-root user
RUN useradd --create-home appuser || true
WORKDIR /app

# Install system deps required by psycopg2-binary (kept minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

# Copy application
COPY app .

# Expose port used by the app
EXPOSE 8000

USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
