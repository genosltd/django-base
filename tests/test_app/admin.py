from django.contrib import admin
from django_base.admin import BaseModelAdmin

from .models import TestModel


@admin.register(TestModel)
class TestModelAdmin(BaseModelAdmin):
    pass
