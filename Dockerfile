FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

ARG PIP_INDEX_URL=https://pypi.org/simple

COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 120 -i "${PIP_INDEX_URL}" -r requirements.txt

COPY app/ app/
COPY data/ data/

EXPOSE 8004

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -fsS http://localhost:8004/_stcore/health || exit 1

CMD ["streamlit", "run", "app/main.py", "--server.port=8004", "--server.address=0.0.0.0", "--server.headless=true"]
