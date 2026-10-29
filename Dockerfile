FROM python:3.11-slim

WORKDIR /app

COPY arceus_server.py .
COPY "SITE WEB" "SITE WEB"

ENV PORT=8080
ENV ARCEUS_ADMIN_KEY=dj2026

EXPOSE 8080

CMD ["python", "arceus_server.py"]
