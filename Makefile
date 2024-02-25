
# Backend Tasks

.PHONY: backend-code-style
backend-code-style:
	docker-compose run --rm api poetry run pycodestyle --statistics --ignore=E501,W503,E902,E711,E203 --count src

.PHONY: backend-setup
backend-setup:
	docker-compose run --rm api poetry install

.PHONY: backend-test-only
backend-test-only:
	docker-compose run --rm api poetry run py.test tests --no-cov

.PHONY: backend-mypy
backend-mypy:
	docker-compose run --rm api poetry run mypy src

.PHONY: backend-black-check
backend-black-check:
	docker-compose run --rm api poetry run black --check --diff src

.PHONY: backend-black
backend-black:
	docker-compose run --rm api poetry run black src

.PHONY: backend-isort-check
backend-isort-check:
	docker-compose run --rm api poetry run isort --ac --check-only src

.PHONY: backend-isort
backend-isort:
	docker-compose run --rm api poetry run isort --ac src

.PHONY: backend-check
backend-check: backend-code-style backend-isort-check backend-black-check backend-mypy

.PHONY: backend-format
backend-format: backend-isort backend-black

.PHONY: backend-test
backend-test: backend-check
	docker-compose run --rm api poetry run py.test tests --cov=. --cov-report xml --cov-report term --cov-report html --cov-fail-under=90


# Frontend Tasks
