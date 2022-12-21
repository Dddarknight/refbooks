lint:
	poetry run flake8

install:
	poetry install

test-coverage:
	poetry run coverage run --source='.' manage.py test
	poetry run coverage report
	poetry run coverage xml

run:
	poetry run python manage.py runserver

test:
	poetry run python manage.py test

migrate:
	poetry run python manage.py migrate
