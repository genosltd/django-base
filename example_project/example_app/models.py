from django.db import models

from django_base.models import BaseModel


class Item(BaseModel):
    example_field = models.CharField(max_length=255)
