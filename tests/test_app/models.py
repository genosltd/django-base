from django.db import models
from django_base.models import BaseModel


class TestModel(BaseModel):
    test_field = models.CharField(max_length=255)
