FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
COPY furniture_store ./furniture_store
COPY reports ./reports
COPY static_dev ./static_dev
COPY staticfiles ./staticfiles
COPY templates ./templates

RUN pip install --no-cache-dir -r requirements.txt

COPY furniture_store/entrypoint.sh
RUN chmod +x furniture_store/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]