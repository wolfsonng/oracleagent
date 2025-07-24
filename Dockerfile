FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libaio1 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Linux Instant Client (for Docker/Linux containers)
COPY instantclient_23_8/ ./oracle/

# Copy application code
COPY app.py config.py oracle_utils.py ./

ENV ORACLE_CLIENT_LIB_DIR=/app/oracle
ENV LD_LIBRARY_PATH=/app/oracle
ENV PYTHONUNBUFFERED=1

EXPOSE 5001

CMD ["python", "app.py"]