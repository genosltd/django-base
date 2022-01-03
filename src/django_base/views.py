import os
import imagehash
from PIL import Image
import uuid

from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import *


def check_similar(phash, similarity=0.1):
    """
    check if simlar image already exists in the database
    adjust the similarity value based on the desired similarity cutoff [0.0 - 1.0]
    0.0 -> eliminate only identical images
    1.0 -> let identical images pass and save copies
    0.1 -> allow for 0.1 similarity between images that are saved
    """

    for i in ImageModel.objects.all(): # use MMImage for ManyToMany | ImageModel for Generic-M2M
        temp = os.path.join(settings.MEDIA_ROOT, i.image.name)

        if (phash - imagehash.phash(Image.open(temp)))/len(phash) <= similarity:
            return JsonResponse({
                'message': 'file already exist',
                'location': f'{settings.MEDIA_URL}{i.image.name}',
            })

    return 


def check_identical(phash):
    """
    compare if image hash already exists in the database
    """

    if phash.__str__() in ImageModel.objects.get_all_img_hashes().values():
        location = ImageModel.objects.get(hash=phash.__str__()).image.name
        return JsonResponse({
            'message': 'file already exist',
            'location': f'{settings.MEDIA_URL}{location}'
        })

    return


@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        file_obj = request.FILES['file']
        file_name_suffix = file_obj.name.split(".")[-1]
        if file_name_suffix not in ["jpg", "png", "gif", "jpeg", ]:
            return JsonResponse({"message": "Wrong file format"})

        upload_time = timezone.now()
        path = os.path.join(
            settings.MEDIA_ROOT,
            'tinymce',
            str(upload_time.year),
            str(upload_time.month),
        )
        # If there is no such path, create it
        if not os.path.exists(path):
            os.makedirs(path)

        file_path = os.path.join(path, file_obj.name)
        file_url = f'tinymce/{upload_time.year}/{upload_time.month}/{file_obj.name}'

        # calculate perceptual hash of the uploaded image
        phash = imagehash.phash(Image.open(file_obj))

        # check if such an image already exists
        if check_identical(phash):
            return check_identical(phash)

        # if an object with the same name already exists, add a random string to the name
        if os.path.exists(file_path):
            temp = file_path.split('.')
            file_path = f'{temp[0]}{"".join(str(uuid.uuid4()).split("-"))}.{temp[1]}'

        # save file inside the path folder
        with open(file_path, 'wb+') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
        
        # return a JSON response with the file location
        return JsonResponse({
            'message': 'Image uploaded successfully',
            'location': f'{settings.MEDIA_URL}{file_url}',
        })

    return JsonResponse({'detail': 'Wrong request'})