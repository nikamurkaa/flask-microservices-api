FROM python:3.12-slim

WORKDIR /app

COPY services/order_service/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY services /app/services
ENV PYTHONPATH=/app
EXPOSE 5002

CMD ["python", "-m", "services.order_service.run"]
