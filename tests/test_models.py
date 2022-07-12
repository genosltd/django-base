from django.test import TestCase
from django.contrib.auth.models import User

from .test_app.models import TestModel


class Setup:
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser(
            username='admin', password='pass'
        )
        cls.user = User.objects.create_user(
            username='user', password='pass', is_staff=True
        )
        cls.usr_obj = TestModel.objects.create(owner=cls.user)
        cls.adm_obj = TestModel.objects.create(owner=cls.admin)


class TestBaseModel(Setup, TestCase):
    def test_remove(self):
        obj = TestModel.objects.create(owner=self.user)
        obj_id = obj.id
        obj.remove()
        with self.assertRaises(TestModel.DoesNotExist):
            TestModel.objects.get(pk=obj_id)

    def test_delete(self):
        obj = self.usr_obj
        obj.delete()
        self.assertFalse(obj.is_active)


class TestBaseQuerySet(Setup, TestCase):
    def test_deactivate(self):
        TestModel.objects.all().deactivate()

        for obj in (self.adm_obj, self.usr_obj):
            del obj.is_active
            self.assertFalse(obj.is_active)

    def test_activate(self):
        TestModel.objects.all().deactivate()

        for obj in (self.adm_obj, self.usr_obj):
            del obj.is_active
            self.assertFalse(obj.is_active)

        TestModel.objects.all().activate()

        for obj in (self.adm_obj, self.usr_obj):
            del obj.is_active
            self.assertTrue(obj.is_active)

    def test_remove(self):
        TestModel.objects.all().remove()
