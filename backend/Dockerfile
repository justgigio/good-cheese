FROM python:3.12.2-slim as base
WORKDIR /app

RUN apt update && apt install libpq-dev gcc -y

RUN pip install poetry==1.7.1

COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY . ./

EXPOSE 8000/tcp
CMD [ "poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--reload" ]
