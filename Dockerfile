FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Copy wait script
COPY wait-for-postgres.sh .
RUN chmod +x wait-for-postgres.sh

# Expose port
EXPOSE 5100

# Wait for postgres, then run migrations and start server
CMD ["./wait-for-postgres.sh", "db"]