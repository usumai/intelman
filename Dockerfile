FROM python:3.10-slim

# Install required system dependencies
RUN apt-get update && apt-get install -y git ffmpeg postgresql-client


WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Clone the markitdown repository and install it
RUN git clone https://github.com/microsoft/markitdown.git /tmp/markitdown
RUN pip install -e /tmp/markitdown/packages/markitdown[all]

# Copy the wait-for-db script from the app folder and make it executable
COPY wait-for-db.sh /app/wait-for-db.sh
RUN chmod +x /app/wait-for-db.sh

# Copy your application code into the container
COPY . .

EXPOSE 5000

# Use the wait-for-db script to ensure the PostgreSQL service is up before starting the app
CMD ["/app/wait-for-db.sh", "db", "python", "app/app.py"]
