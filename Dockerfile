FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY README.md .

ENV PHILIXA_DATABASE_URL=sqlite:////app/data/philixa.db
ENV PHILIXA_API_KEY=dev-api-key
ENV PHILIXA_AI_PROVIDER=local

RUN mkdir -p /app/data

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
