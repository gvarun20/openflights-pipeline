# -----------------------------------------------------------------------------
# Stage 1 — builder: install Python dependencies (cached layer)
# -----------------------------------------------------------------------------
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

# -----------------------------------------------------------------------------
# Stage 2 — runtime: copy deps + app code, run as non-root user
# -----------------------------------------------------------------------------
FROM python:3.11-slim AS runtime

RUN groupadd --system appuser && useradd --system --gid appuser appuser

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

RUN mkdir -p logs && chown -R appuser:appuser /app

USER appuser

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

CMD ["python", "-m", "etl.run_etl", "--help"]
