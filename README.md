# Setup

Create a `.env` file using `.env.example` as model:

```
$ cp .env.example .env
```

Build docker images:

```
$ docker-compose build
```

Run backend setup:

```
$ docker-compose run --rm api python db_setup.py
```

Run database migrations:

```
$ docker-compose run --rm api poetry run alembic upgrade head
```

Run project:

```
$ docker-compose up
```

The App should be available at [http://localhost:8888](http://localhost:8888)

- Processing a ~100MB file in less than 60 seconds :white_check_mark: (Actually around 17s)

# Sending boleto e-mails

After upload at least 1 CSV file, you can run the task:

```
$ docker-compose exec api poetry run python
Python 3.12.2 (main, Feb 13 2024, 09:28:52) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from src.tasks import process_boletos
>>> process_boletos.apply_async()
```

You can check some movement in celery container log. You can also check the e-mails arriving into Mailhog inbox: [http://localhost:8025](http://localhost:8025)

>*Note:* The boleto generator is only a mock with 0.1s sleep to simulate a call for an external API.

# TODO
 - Tests
 - Move some code outside from component
 - Some data validation
 - Handle some edge cases
 - Actualy generate boletos
