FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System deps for common Python package builds/runtime.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install only MLOps app dependencies (Gemini stack intentionally excluded).
COPY requirements-mlops.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-mlops.txt

COPY . .

# Azure App Service sets PORT dynamically; default is useful for local containers.
ENV PORT=8000
EXPOSE 8000

# Gunicorn production entrypoint.
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT} --workers 2 --timeout 120 wsgi:app"]

