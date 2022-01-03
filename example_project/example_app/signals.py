from django.db.models import signals
from django.db import transaction
from django.dispatch import receiver

import os
from . models import MMExample, ImageModel


# M2M images.add does not work with post_save or pre_save signals
# need transaction.on_commit wrapper to work properly
def on_transaction_commit(func):
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))

    return inner

@receiver(signals.post_save, sender=MMExample)
@on_transaction_commit
def update_m2m_relationship(sender, instance, *args, **kwargs):
    """
    Update ManyToMany relationship between ExampleModel and ImageModel
    """

    unique = []
    hashes = [hash.__str__() for hash in instance.get_all_img_hashes()]
    images = instance.get_all_images()
    names = [os.path.basename(image).split('.')[0] for image in images]

    instance.images.clear()

    for i, image in enumerate(images):
        if hashes[i] not in unique:
            if hashes[i] in ImageModel.objects.get_all_img_hashes().values():
                to_add = ImageModel.objects.get(hash=hashes[i])
                instance.images.add(to_add)
                unique.append(hashes[i])

            else:
                image_object = ImageModel.objects.create(image=image, hash=hashes[i], name=names[i])
                instance.images.add(image_object)
                unique.append(hashes[i])
