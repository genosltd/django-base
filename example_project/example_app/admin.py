from django.contrib import admin
from django.utils.html import mark_safe

from django_base.admin import BaseModelAdmin, ImageItemInline
from .models import *

from bs4 import BeautifulSoup



@admin.register(ExampleModel)
class ExampleModelAdmin(BaseModelAdmin):
    class Media:
        css = {"all" : ("css/override_admin.css",)}
    
    inlines = (ImageItemInline,)

    list_display = ('id', 'example_label', 'user', 'created', 'modified', 'uuid', )
    ordering = ('id',)

    def example_label(self, obj):
        if obj.example is not None:
            soup = BeautifulSoup(obj.example, 'html.parser')
            text = [txt.getText() for txt in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']) if txt.getText().strip()]
            img = soup.find_all('img')

            if text:
                return text[0][0:50]
            elif img:
                return mark_safe(" | ".join([f'<img src="{image["src"]}" width="75" height="75" />' for image in img[:3]]))
            else:
                return "Placeholder"
        else:
            return "Enter text here..."

    example_label.short_description = "Label"


# M2M implementation
class ImageModelInline(admin.TabularInline):

    model = MMExample.images.through
    label = None
    can_delete = False
    extra = 0
    max_num = 0
    show_change_link = False
    # template = 'image_inline.html'
    fields = ['img_link']
    readonly_fields = ['img_link',]

    def img_link(self, instance):
        return mark_safe(f'<a href="/admin/django_base/imagemodel/{instance.imagemodel.id}/change">{instance.imagemodel.name}</a>')

    img_link.short_description = "Image Link"

    def has_change_permission(self, request, obj=None):
        return False


# inherits from ExampleModelAdmin
@admin.register(MMExample)
class MMExampleAdmin(ExampleModelAdmin):
    class Media:
        css = { "all" : ("css/override_admin.css",) }

    inlines = (ImageModelInline, )

    fields = ('example',)

