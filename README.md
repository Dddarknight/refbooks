# refbooks

The application provides API for dealing with reference books.

Endpoints:

| Endpoint | Method | Description |
|----------|---------|---------|
| /refbooks/ [?date=<date>] | GET |  Returns all availible refbooks. If a date parameter is provided, only refbooks which have versions with started date after the requested date will be returned. |
| /refbooks/{id}/elements [?version={version}] | GET | Returns elements of the requested refbook in the latest version. If a version parameter provided, only elements of this version of the RefBook will be returned. |
| /refbooks/{id}/check_element?code={code}&value={value} [&version={version}] | GET |  Check if the element with provided parameters exists. If a version parameter is absent, the element will be checked in the latest version. |
| /docs | GET |  API documentation with Swagger/OpenAPI 2.0 specifications. |
| /admin | GET |  Admin interface. |


<a href="https://codeclimate.com/github/Dddarknight/refbooks/test_coverage"><img src="https://api.codeclimate.com/v1/badges/e34fc047b0cdae42c43e/test_coverage" /></a>

## Links
This project was built using these tools:
| Tool | Description |
|----------|---------|
| [Django ](https://www.djangoproject.com/) |  "A high-level Python web framework" |
| [Django REST framework](https://www.django-rest-framework.org/) |  "A powerful and flexible toolkit for building Web APIs" |
| [drf-yasg](https://drf-yasg.readthedocs.io/en/stable/readme.html) |  "Generate real Swagger/OpenAPI 2.0 specifications from a Django Rest Framework API." |
| [poetry](https://python-poetry.org/) |  "Python dependency management and packaging made easy" |

## Installation
**Copy a project**

```
$ git clone git@github.com:Dddarknight/refbooks.git
$ cd refbooks
```

**Set up environment variables**
```
$ touch .env

You have to write into .env file SECRET_KEY for Django app. See .env.example.
To get SECRET_KEY for Django app:
$ python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> get_random_secret_key()

Then add new SECRET_KEY to .env file
```

**Set up the environment**
```
$ pip install poetry
$ make install
```

**Dealing with migrations**
```
$ make migrate
```

**Launch**
```
$ make run
```

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)