FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# No EXPOSE/hardcoded port — Railway injects $PORT at runtime.
# Shell form (not exec/array form) is required so $PORT actually expands.
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
