from django.db import models
from django.contrib.auth.models import User
from simple_history import register

from django_base.models import BaseModel


register(User, app=__package__)


class Item(BaseModel):
    example_field = models.CharField(max_length=255)
