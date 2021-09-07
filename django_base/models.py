from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from simple_history.models import HistoricalRecords

import uuid

class BaseModel(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    history = HistoricalRecords(inherit=True)
