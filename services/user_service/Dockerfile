FROM python:3.12-slim

WORKDIR /app

COPY services/user_service/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY services /app/services
ENV PYTHONPATH=/app
EXPOSE 5001

CMD ["python", "-m", "services.user_service.run"]
