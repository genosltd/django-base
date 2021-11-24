from django.db import models

from django_base.models import BaseModel


class ExampleModel(BaseModel):
    example = models.TextField(null=True, blank=True)
