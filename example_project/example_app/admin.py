from django.contrib import admin

from django_base.admin import BaseModelAdmin
from .models import Item


@admin.register(Item)
class ItemAdmin(BaseModelAdmin):
    pass
