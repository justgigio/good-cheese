# Setup

Create a `.env` file inside `backend` folder using `.env.example` as model:

```
$ cp backend/.env.example backend/.env
```

Build docker images:

```
$ docker-compose build
```

Install frontend deps

```
$ make frontend-setup
```

Run backend setup:

```
$ make backend-setup
```

Run project:

```
$ docker-compose up
```

The App should be available at [http://localhost:8888](http://localhost:8888)

The API doc should be available at [http://localhost:8000/docs](http://localhost:8000/docs)

- Processing a `~100MB` file with `1,100,000` lines in less than 60 seconds :white_check_mark: (Actually around 5s !!! :fire:)

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

# Testing

Just run

```
$ make test
```

To run front or back separatedely, you can run:
```
$ make frontend-test
```
Or
```
$ make backend-test
```

# TODO
 - Tests Coverage 90%+
 - Front Tests (Unfortunately cannot be done with Bun yet :sob: [https://github.com/oven-sh/bun/issues/198](https://github.com/oven-sh/bun/issues/198))
 - E2E Tests
 - Front Docs
 - Move some code outside from component
 - Some data validation
 - Pagination
 - Handle some edge cases
 - Actualy generate boletos
