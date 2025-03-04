FROM python:3.12-slim

RUN useradd --create-home appuser
WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY start.sh .
RUN chmod +x start.sh

COPY . .
USER appuser
ENTRYPOINT ["./start.sh"]
