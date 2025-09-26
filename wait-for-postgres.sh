#!/bin/bash
# wait-for-postgres.sh

set -e

host="$1"
shift
cmd="$@"

echo "🔄 Waiting for PostgreSQL at $host:5432..."

until nc -z "$host" 5432; do
  echo "⏳ PostgreSQL is unavailable - sleeping"
  sleep 2
done

echo "✅ PostgreSQL is up - executing command"

# Wait a bit more to ensure PostgreSQL is fully ready
sleep 5

# Run migrations
echo "🔄 Running migrations..."
python manage.py makemigrations users --noinput
python manage.py makemigrations requests --noinput
python manage.py migrate --noinput

echo "🚀 Starting Django server..."
exec python manage.py runserver 0.0.0.0:5100