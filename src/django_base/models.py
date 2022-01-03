from django.db import models
from django.conf import settings
from django.utils.html import mark_safe
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group, Permission

import os
from bs4 import BeautifulSoup
from PIL import Image
import imagehash
import uuid

from simple_history.models import HistoricalRecords
import simple_history

from django_hashtag.models import HasHashtags
from django_comment.models import HasComments


simple_history.register(User, app=__package__)
simple_history.register(Group, app=__package__)
simple_history.register(Permission, app=__package__)


class BaseModel(HasHashtags, HasComments):
    class Meta:
        abstract = True

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    history = HistoricalRecords(inherit=True)


def update_generic_relationship(sender, instance, *args, **kwargs):
    """
    Update Generic relationship between ExampleModel and ImageModel
    """
     
    unique = []
    # all img hashes inside a TinyMCE TextField
    hashes = [hash.__str__() for hash in instance.get_all_img_hashes()]
    # all images inside a TextField
    images = instance.get_all_images()
    # names of the images
    names = [os.path.basename(image).split('.')[0] for image in images]

    # clear images connected to the ExampleModel
    instance.images.clear()

    for i, image in enumerate(images):
        if hashes[i] not in unique:
            if hashes[i] in ImageModel.objects.get_all_img_hashes().values():
                imagemodel = ImageModel.objects.get(hash=hashes[i])
            else:
                imagemodel = ImageModel.objects.create(image=image, hash=hashes[i], name=names[i])

            instance.images.add(imagemodel)
            unique.append(hashes[i])


class ImageManager(models.Manager):
    def get_all_img_hashes(self):
        dict = {}
        for image in super().get_queryset():
            try:
                dict[image.image.name] = imagehash.phash(Image.open(image.image)).__str__()
            except:
                dict[image.image.name] = None
        
        return dict


class ImageModel(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=255)
    hash = models.CharField(max_length=64)

    objects = ImageManager()

    def __str__(self):
        return self.image.name

    @property
    def img_preview(self):
        if self.image:
            return mark_safe(f'<img src="/media/{self.image}" width="100" height="100" />')
        return "No Image"


class ImageItem(models.Model):
    images = models.ManyToManyField(ImageModel, related_name='image_item', blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, editable=False)
    object_id = models.PositiveIntegerField(editable=False)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        string =  "; ".join([img.name for img in self.images.all()])

        if len(string) <= 50:
            return string
        else:
            return f'{string[:50]}...'


class HasImage(models.Model):
    class Meta:
        abstract = True

    imageitems = GenericRelation(ImageItem, blank=True)

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        models.signals.post_save.connect(update_generic_relationship, sender=cls)

    def get_hash_from_html(self, image_url):
        temp = os.path.join(settings.MEDIA_ROOT, image_url.split('media/')[-1])
        phash = imagehash.phash(Image.open(temp))

        return phash
    
    def get_all_img_hashes(self):
        soup = BeautifulSoup(self.example, 'html.parser')
        img_hashes = list(map(self.get_hash_from_html, [img['src'] for img in soup.find_all('img')]))
        
        return img_hashes

    def get_all_images(self):
        soup = BeautifulSoup(self.example, 'html.parser')
        images = [img['src'].split('media/')[-1] for img in soup.find_all('img')]

        return images

    @property
    def images(self):
        try:
            return self.imageitems.first().images

        except AttributeError:
            return self.imageitems.create().images
