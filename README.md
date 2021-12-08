# Django Base

## Installation

~~~
> pipenv install https://github.com/genosltd/django-base
~~~

or with pip:

~~~
> pip install https://github.com/genosltd/django-base
~~~

## Usage

Do not forget to list `django_base` and requirements in `settings.py`:

~~~python
# settings.py
INSTALLED_APPS = [
    'simple_history',
    'django_hashtag',
    'django_comment',

    'django_base',
]
~~~

### Models

~~~python
# models.py
from django import models
from django_base.models import BaseModel

class MyModel(BaseModel):
    my_field = models.CharField()
~~~

### Admin

~~~python
# admin.py
from django.contrib import admin
from django_base.admin import BaseModelAdmin
from .models import MyModel

@admin.register(MyModel)
class MyModelAdmin(BaseModelAdmin):
    pass
~~~

## Contributing

1. Document the problem you are contributing to by [creating a new issue][new-issue] if not documented already.
1. Fork the repo privately [here][fork]. See [Fork a repo][fork-a-repo] for help.
1. Clone you fork locally. See [Cloning a repository][clone-a-repo] for help.
1. Open your clone directory in `cmd`
1. Install `django-base` with:

    ~~~
    > pipenv install --skip-lock -d
    ~~~

1. Optionally for faster dev cycle, install venv with python 3.7:

    ~~~
    > python -m venv venv && venv\Scripts\activate.bat

    (venv)> python -m pip install -U pip  && pip install --no-deps -r requirements.txt && pip install -e .
    ~~~

1. Create a new branch
1. Make necessary changes to the code
1. Test your changes as described in [Testing][]
1. Commit and push
1. Create pull request
1. Discuss and tweak your contribution
1. Celebrate

### Testing

For testing please use:

~~~
> pipenv run runtests.py
~~~

or with venv:

~~~
> venv\Scripts\activate.bat && python runtests.py
~~~

For coverage use:

~~~
> pipenv run coverage run && pipenv run coverage html
~~~

or with venv:

~~~
> venv\Scripts\activate.bat && coverage run && coverage html
~~~

Open [index.html](.\htmlcov\index.html]) in your browser for the coverage report.

[new-issue]: https://github.com/genosltd/django-base/issues/new
[fork]: https://github.com/genosltd/django-base/fork
[fork-a-repo]: https://docs.github.com/en/get-started/quickstart/fork-a-repo
[clone-a-repo]: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository
