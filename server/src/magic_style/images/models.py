import uuid

from django.db import models

from utils.constants.images import ImageTypeEnum


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    upload_name = models.CharField(null=True, max_length=100)
    now_name = models.CharField(max_length=32)
    image_type = models.CharField(default=ImageTypeEnum.other, max_length=32)
    create_time = models.DateTimeField(auto_now_add=True)


class UploadImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    upload_name = models.CharField(null=True, max_length=100)
    now_name = models.CharField(max_length=32)
    create_time = models.DateTimeField(auto_now_add=True)


class GenerateImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    now_name = models.CharField(max_length=32)
    create_time = models.DateTimeField(auto_now_add=True)
