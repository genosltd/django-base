from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib import admin
from django.urls import reverse

from .test_app.models import TestModel
from .test_app.admin import TestModelAdmin


class TestBaseModelAdmin(TestCase):
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

    def setUp(self):
        self.factory = RequestFactory()
        self.testmodeladmin = TestModelAdmin(TestModel, admin.site)

    def get_request(self, url='admin:index', **kwargs):
        return self.factory.get(reverse(url, kwargs=kwargs))

    def test_can_remove(self):
        request = self.get_request()
        request.user = self.user
        self.assertFalse(self.testmodeladmin.can_remove(request))

        request.user = self.admin
        self.assertTrue(self.testmodeladmin.can_remove(request))

    def test_can_change_owner(self):
        request = self.get_request()
        request.user = self.user
        self.assertFalse(self.testmodeladmin.can_change_owner(request))

        request.user = self.admin
        self.assertTrue(self.testmodeladmin.can_change_owner(request))

    def test_get_readonly_fields(self):
        request = self.get_request('admin:test_app_testmodel_add')

        request.user = self.admin
        readonly_fields = self.testmodeladmin.get_readonly_fields(request)
        self.assertEqual(set(readonly_fields), set(('uuid', 'created_on', 'modified_on')))

        request.user = self.user
        readonly_fields = self.testmodeladmin.get_readonly_fields(request)
        self.assertIn('owner', readonly_fields)

    def test_get_fieldsets(self):
        request = self.get_request('admin:test_app_testmodel_add')
        request.user = self.user

        fieldsets = self.testmodeladmin.get_fieldsets(request)
        self.assertIn('test_field', fieldsets[0][1]['fields'])
        self.assertEqual(self.testmodeladmin._fieldsets[0], fieldsets[-1])

    def test_get_changeform_initial_data(self):
        request = self.get_request('admin:test_app_testmodel_add')
        request.user = self.user

        data = self.testmodeladmin.get_changeform_initial_data(request)
        self.assertEqual(data['owner'], self.user)

    def test_get_ordering(self):
        request = self.get_request('admin:test_app_testmodel_changelist')
        request.user = self.user

        ordering = self.testmodeladmin.get_ordering(request)
        self.assertEqual(list(ordering), ['-is_active'])

    def test_list_filter(self):
        request = self.get_request('admin:test_app_testmodel_changelist')
        request.user = self.user

        list_filter = self.testmodeladmin.get_list_filter(request)
        self.assertEqual(list(list_filter), ['is_active'])

    def test_delete_model(self):
        request = self.get_request('admin:test_app_testmodel_delete', object_id=1)

        request.user = self.user
        self.testmodeladmin.delete_model(request, self.usr_obj)
        self.assertFalse(self.usr_obj.is_active)

        request.user = self.admin
        self.testmodeladmin.delete_model(request, self.usr_obj)
        with self.assertRaises(TestModel.DoesNotExist):
            TestModel.objects.get(pk=self.usr_obj.id)

    def test_delete_queryset(self):
        request = self.get_request('admin:test_app_testmodel_changelist')
        queryset = TestModel.objects.all()

        request.user = self.user
        self.testmodeladmin.delete_queryset(request, queryset)
        for obj in (self.usr_obj, self.adm_obj):
            del obj.is_active
            self.assertFalse(obj.is_active)

        request.user = self.admin
        self.testmodeladmin.delete_queryset(request, queryset)
        self.assertFalse(queryset.exists())
