from django.contrib import admin

from django_base.admin import BaseModelAdmin
from .models import ExampleModel


@admin.register(ExampleModel)
class ExampleModelAdmin(BaseModelAdmin):
    pass
