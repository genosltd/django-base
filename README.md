# Django Base

## Installation

~~~
> pipenv install https://github.com/genosltd/django-base
~~~

## Usage

Do not forget to list `django-base` in `settings.py`:

~~~python
# settings.py
INSTALLED_APPS = [
    'django-base',
]
~~~

### Models

### Admin


### Testing

For testing please use:

~~~
> pipenv run tests\runtests.py
~~~

or with coverage:

~~~
> pipenv run coverage run --source django_base tests\runtests.py
~~~

and then for html coverage report (in `htmlcov`):

~~~
> pipenv run coverage html
~~~

