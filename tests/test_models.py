from django.test import TestCase

# from django_base import models
from tests.test_app.models import TestModel
from django.contrib.auth.models import User

from datetime import datetime


class BaseModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.created = datetime.now()
        cls.user = User.objects.create(username='user')
        cls.instance = TestModel.objects.create(user=cls.user)

    def test_user(self):
        self.assertEqual(self.instance.user, self.user)

    def test_created(self):
        self.assertGreaterEqual(self.instance.created, self.created)

    def test_modified(self):
        modified = datetime.now()

        self.instance.test_field = 'modified test field'
        self.instance.save()

        self.assertGreaterEqual(self.instance.modified, modified)
