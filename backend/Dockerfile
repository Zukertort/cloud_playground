FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    libpq-dev \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Compile C++ Engine
RUN pip install .

# Explicit copy for the script
COPY scripts/start.sh /start.sh

RUN dos2unix /start.sh && chmod +x /start.sh

EXPOSE 8000

CMD ["bash", "/start.sh"]