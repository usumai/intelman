FROM python:3.10-slim

# Install required system dependencies
RUN apt-get update && apt-get install -y git ffmpeg postgresql-client

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Clone the markitdown repository and install it
RUN git clone https://github.com/microsoft/markitdown.git /tmp/markitdown
RUN pip install -e /tmp/markitdown/packages/markitdown[all]

# Copy the wait-for-db script
COPY wait-for-db.sh /app/wait-for-db.sh
RUN chmod +x /app/wait-for-db.sh

# Copy the entire app folder
COPY . .

# Expose FastAPI’s port
EXPOSE 5000

# Use wait-for-db.sh to ensure the database is up, then start Uvicorn
CMD ["/app/wait-for-db.sh", "db", "uvicorn", "app.main:app", "--host=0.0.0.0", "--port=5000"]
