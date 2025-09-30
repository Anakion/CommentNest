FROM python:3.13-slim

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY . .

RUN uv pip install --system --no-cache .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
