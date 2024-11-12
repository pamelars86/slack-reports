# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN pip install poetry && poetry install

COPY . /app

# Exponha a porta que o Flask usará
EXPOSE 5000

CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0"]