from django.db import models

from django_base.models import BaseModel

from tinymce.models import HTMLField

class ExampleModel(BaseModel):
    example = HTMLField(null=True, blank=True)
