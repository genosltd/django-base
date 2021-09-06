from django.db import models
from django_base import models as django_base_models


class TestModel(django_base_models.BaseModel):
    test_field = models.CharField(max_length=100)
