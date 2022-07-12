from django.db import models
from django.conf import settings

import uuid


class BaseQuerySet(models.QuerySet):
    def deactivate(self):
        self.update(is_active=False)

    def activate(self):
        self.update(is_active=True)

    delete = deactivate

    def remove(self):
        super().delete()


class BaseModel(models.Model):
    class Meta:
        abstract = True
        permissions = (
            ('can_remove', 'Can remove item'),
            ('can_change_owner', 'Can change owner')
        )

    is_active = models.BooleanField(default=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    objects = BaseQuerySet.as_manager()

    def remove(self, **kwargs):
        super().delete(**kwargs)

    def delete(self, **kwargs):
        self.is_active = False
        self.save()
