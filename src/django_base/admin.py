# from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin


class BaseModelAdmin(SimpleHistoryAdmin):
    basic_fields = ('uuid', 'owner', 'created_on', 'modified_on', 'is_active')
    _list_filter = ('is_active',)
    _ordering = ('-is_active',)
    _readonly_fields = ('created_on', 'modified_on', 'uuid')
    _fieldsets = (
        ('Basic info', {
            'classes': ('collapse',),
            'fields': ('uuid', 'owner', 'created_on', 'modified_on',
                       'is_active')
        }),
    )

    def can_remove(self, request, obj=None):
        can_remove = request.user.has_perm('django_base.can_remove', obj)
        is_superuser = request.user.is_superuser

        if can_remove or is_superuser:
            return True
        else:
            return False

    def can_change_owner(self, request, obj=None):
        can_change_owner = request.user.has_perm(
            'django_base.can_change_owner', obj
        )
        is_superuser = request.user.is_superuser

        if can_change_owner or is_superuser:
            return True
        else:
            return False

    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super().get_fieldsets(request, obj=obj))
        if len(fieldsets) == 1:
            fieldset = fieldsets[0]
            fields = list(fieldset[1]['fields'])
            for field in self.basic_fields:
                fields.remove(field)
            fieldset[1]['fields'] = tuple(fields)
            fieldsets = [tuple(fieldset)]

        fieldsets += list(self._fieldsets)
        return fieldsets

    def get_changeform_initial_data(self, request):
        data = super().get_changeform_initial_data(request)
        if 'owner' not in data:
            data['owner'] = request.user
        return data

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = set(super().get_readonly_fields(request, obj=obj))
        readonly_fields.update(set(self._readonly_fields))
        if not self.can_remove(request, obj):
            readonly_fields.add('is_active')

        if not self.can_change_owner(request, obj=obj):
            readonly_fields.add('owner')

        return readonly_fields

    def get_ordering(self, request):
        ordering = list(self._ordering)
        ordering += list(super().get_ordering(request))
        return ordering

    def get_list_filter(self, request):
        list_filter = list(super().get_list_filter(request))
        list_filter += list(self._list_filter)
        return list_filter

    def delete_model(self, request, obj):
        if self.can_remove(request, obj):
            obj.remove()

        else:
            super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        if self.can_remove(request):
            queryset.remove()

        else:
            super().delete_queryset(request, queryset)
