from simple_history.admin import SimpleHistoryAdmin

from django.db.models import TextField
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import mark_safe
from django_hashtag.admin import HasHashtagsAdmin
from django_comment.admin import HasCommentsAdmin

import functools
from tinymce.widgets import TinyMCE

from . models import ImageItem, ImageModel

class _BaseModelAdmin(SimpleHistoryAdmin):
    @staticmethod
    def extend_with(attr):
        def _extend_with(get_attr):
            @functools.wraps(get_attr)
            def wrapper(self, request, obj=None):
                if obj is None:
                    values = list(get_attr(self, request))
                else:
                    values = list(get_attr(self, request, obj))

                for field in attr:
                    if field not in values:
                        values.append(field)

                return tuple(values)

            return wrapper
        return _extend_with


class BaseModelAdmin(HasHashtagsAdmin, HasCommentsAdmin, _BaseModelAdmin):
    readonly_fields = ('created', 'modified', 'uuid')

    @_BaseModelAdmin.extend_with(readonly_fields)
    def get_readonly_fields(self, request, obj=None):
        return super().get_readonly_fields(request, obj)

    list_display = ('user', 'created', 'modified')

    @_BaseModelAdmin.extend_with(list_display)
    def get_list_display(self, request):
        return super().get_list_display(request)

    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name'
    )

    @_BaseModelAdmin.extend_with(search_fields)
    def get_search_fields(self, request):
        return super().get_search_fields(request)

    list_filter = ('user', 'created', 'modified')

    @_BaseModelAdmin.extend_with(list_filter)
    def get_list_filter(self, request):
        return super().get_list_filter(request)

    _fields = ('user', 'created', 'modified', 'uuid')

    def get_fields(self, request, obj=None):
        fields = tuple(super().get_fields(request, obj))
        if fields == BaseModelAdmin._fields:
            return tuple()
        else:
            return fields

    _fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'created', 'modified', 'uuid'),
            'classes': ('collapse',)
        }),
    )

    @_BaseModelAdmin.extend_with(_fieldsets)
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if fieldsets[0][0] is None:
            fields = list(fieldsets[0][1]['fields'])
            for field in fieldsets[0][1]['fields']:
                if field in BaseModelAdmin._fields:
                    fields.remove(field)
            fieldsets[0][1]['fields'] = tuple(fields)

        return fieldsets

    def get_changeform_initial_data(self, request):
        data = super().get_changeform_initial_data(request)
        if 'user' not in data:
            data['user'] = request.user

        return data

    formfield_overrides = {
        TextField: {'widget': TinyMCE()}
    }


class ImageItemInline(GenericTabularInline):

    model = ImageItem
    can_delete = False
    extra = 0
    max_num = 0

    fields = ['img_link',]
    readonly_fields = ['img_link',]

    def img_link(self, instance):
        return mark_safe(" | ".join([
            f'<a href="/admin/django_base/imagemodel/{img.id}/change">{img.name}</a>' for img in ImageItem.objects.get(object_id=instance.object_id).images.all()
        ]))

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(ImageModel)
class ImageModelAdmin(admin.ModelAdmin):
    fields = ('name', 'image', 'hash', 'img_preview', )
    list_display = ('name', 'img_preview', 'image', 'hash', )

    def has_change_permission(self, request, obj=None):
        return False

    def image_tag(self):
        return mark_safe(f'<img src="{self.image}"/>')
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def img_preview(self, obj):
        return obj.img_preview

        