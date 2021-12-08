from django.contrib import admin

from django_base.admin import BaseModelAdmin
from .models import ExampleModel
from django.db import models

from tinymce.widgets import TinyMCE

@admin.register(ExampleModel)
class ExampleModelAdmin(BaseModelAdmin):
    pass