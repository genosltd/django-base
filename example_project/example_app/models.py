from django.db import models

from django_base.models import *

from tinymce.models import HTMLField


# Implementation of a generic many-to-many relationship with imagemodel
class ExampleModel(BaseModel, HasImage):
    example = HTMLField(null=True, blank=True)

    def __str__(self) -> str:
        return "; ".join([img.name for img in self.images.all()]) if self.images.all() else "No Images"

# Implementation of a many-to-many relationship with imagemodel
class MMExample(BaseModel, HasImage):
    example = HTMLField(null=True, blank=True)
    images = models.ManyToManyField(ImageModel, blank=True) # override images field from HasImages class

    def __str__(self) -> str:
        return "; ".join([img.name for img in self.images.all()])


# disconnect update_generic_relationship signal from HasImage __init_subclass__ method
# MMExample inherits from HasImage methods that are needed for generic many-to-many relationship
# but sometimes break standard many-to-many relationship from working properly
models.signals.post_save.disconnect(update_generic_relationship, sender=MMExample) 

