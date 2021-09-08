from django.test import TestCase, RequestFactory
from django.urls import reverse

# from django_base import models
from test_app.models import TestModel
from test_app.admin import TestModelAdmin
from django.contrib.auth.models import User

from django.contrib import admin


class BaseModelAdminTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='user')
        cls.instance = TestModel.objects.create(user=cls.user)
        cls.request_factory = RequestFactory()

    def test_extend_with_from_empty(self):
        url = reverse('admin:test_app_testmodel_changelist')
        request = self.request_factory.get(url)
        base_modeladmin = TestModelAdmin(TestModel, admin.site)
        list_display = base_modeladmin.get_list_display(request)
        self.assertEqual(list_display, ('user', 'created', 'modified'))

    def test_extend_with_from_full(self):
        url = reverse('admin:test_app_testmodel_changelist')
        request = self.request_factory.get(url)
        base_modeladmin = TestModelAdmin(TestModel, admin.site)
        base_modeladmin.list_display = ('test',)
        list_display = base_modeladmin.get_list_display(request)
        self.assertEqual(list_display, ('test', 'user', 'created', 'modified'))

    def test_extend_with_for_single_obj(self):
        instance = self.instance
        url = reverse('admin:test_app_testmodel_change', args=(instance.id,))
        request = self.request_factory.get(url)
        request.user = self.user
        base_modeladmin = TestModelAdmin(TestModel, admin.site)
        fieldsets = base_modeladmin.get_fieldsets(request, obj=instance)
        self.assertEqual(fieldsets[-1], (
            'Basic Info', {
                'fields': ('user', 'created', 'modified', 'uuid'),
                'classes': ('collapse',)
            })
        )

    def test_get_search_fields(self):
        url = reverse('admin:test_app_testmodel_changelist')
        request = self.request_factory.get(url)
        base_modeladmin = TestModelAdmin(TestModel, admin.site)
        search_fields = base_modeladmin.get_search_fields(request)
        self.assertEqual(search_fields, ('user__username', 'user__first_name',
                                         'user__last_name'))

    def test_get_list_filter(self):
        url = reverse('admin:test_app_testmodel_changelist')
        request = self.request_factory.get(url)
        base_modeladmin = TestModelAdmin(TestModel, admin.site)
        list_filter = base_modeladmin.get_list_filter(request)
        self.assertEqual(list_filter, ('user', 'created', 'modified'))

    def test_get_fields_default(self):
        instance = self.instance
        url = reverse('admin:test_app_testmodel_change', args=(instance.id,))
        request = self.request_factory.get(url)
        request.user = self.user
        base_modeladmin = TestModelAdmin(TestModel, admin.site)
        base_modeladmin.exclude = ('test_field',)
        fields = base_modeladmin.get_fields(request, obj=instance)

        self.assertEqual(fields, tuple())

    def test_get_readonly_fields(self):
        instance = self.instance
        url = reverse('admin:test_app_testmodel_change', args=(instance.id,))
        request = self.request_factory.get(url)
        request.user = self.user
        base_modeladmin = TestModelAdmin(TestModel, admin.site)
        readonly_fields = base_modeladmin.get_readonly_fields(request,
                                                              obj=instance)

        self.assertEqual(readonly_fields, ('created', 'modified', 'uuid'))

    def test_get_changeform_initial_data(self):
        url = reverse('admin:test_app_testmodel_add')
        request = self.request_factory.get(url)
        request.user = self.user
        base_modeladmin = TestModelAdmin(TestModel, admin.site)
        initial_data = base_modeladmin.get_changeform_initial_data(request)

        self.assertEqual(initial_data, {'user': self.user})
