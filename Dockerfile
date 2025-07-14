FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r <(python - <<'PY'
import toml
print('\n'.join(toml.load('pyproject.toml')['project']['dependencies']))
PY
)

COPY src/ ./src
COPY dags/ ./dags

ENV PYTHONUNBUFFERED=1
CMD ["airflow", "standalone"]
