from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.models import User, Group, Permission

from simple_history.models import HistoricalRecords
import simple_history

from django_hashtag.models import HasHashtags
from django_comment.models import HasComments

import uuid


simple_history.register(User, app=__package__)
simple_history.register(Group, app=__package__)
simple_history.register(Permission, app=__package__)


class BaseModel(HasHashtags, HasComments):
    class Meta:
        abstract = True

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    history = HistoricalRecords(inherit=True)
