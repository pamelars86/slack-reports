
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && apt-get clean

WORKDIR /app

COPY . /app

RUN ls -la /app


RUN pip install poetry
RUN poetry install --only main --no-root
# RUN poetry install --no-dev

RUN poetry show

EXPOSE 5000

CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0"]