FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    libpq-dev \
    libomp-dev\
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/requirements.txt ./backend/
COPY pipeline/requirements.txt ./pipeline/

RUN pip install --no-cache-dir -r backend/requirements.txt && \
    pip install --no-cache-dir -r pipeline/requirements.txt

COPY backend/ ./backend/
COPY pipeline/ ./pipeline/

WORKDIR /app/backend
RUN pip install .

COPY backend/scripts/start.sh /start.sh
RUN dos2unix /start.sh && chmod +x /start.sh

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["bash", "/start.sh"]
