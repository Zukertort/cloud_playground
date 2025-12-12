#!/bin/bash
set -e

DB_HOST="db"
DB_PORT="5432"
echo "Waiting for Postgres at $DB_HOST:$DB_PORT..."
while ! python -c "import socket; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(1); s.connect(('$DB_HOST', int('$DB_PORT')))" 2>/dev/null; do
  sleep 1
  echo "Still waiting for Postgres..."
done
echo "Postgres is UP!"


echo "Runnning Alembic Migrations..."


if [ -z "$(ls -A /app/backend/scripts/alembic/versions)" ]; then
   echo "Generating initial migration..."
   cd /app/backend
   alembic revision --autogenerate -m "init_fresh"
fi


cd /app/backend
alembic upgrade head


if [ ! -f "/app/data/models/AAPL_primary.json" ]; then
    echo "COLD START DETECTED: No models found."
    echo "Triggering Initial Pipeline Run (Ingest -> Train)..."
    
    cd /app/pipeline
    python run_pipeline.py
    
    echo "Pipeline Finished. Data hydrated."
    cd /app/backend
else
    echo "Data found. Skipping pipeline."
fi

echo "Starting Server..."
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app -b 0.0.0.0:8000