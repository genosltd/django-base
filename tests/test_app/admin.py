from django.contrib import admin
from django_base.admin import BaseModelAdmin

from test_app.models import TestModel


@admin.register(TestModel)
class TestModelAdmin(BaseModelAdmin):
    pass
