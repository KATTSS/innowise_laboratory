FROM python:3.10-slim-bookworm

WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy dependencies fole
COPY pyproject.toml poetry.lock* ./

# No virtual environment in the container
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main --no-root

# Copy other files from current directory
COPY . .

# Start the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]