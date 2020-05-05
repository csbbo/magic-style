from functools import reduce
from operator import or_

import grpc
from django.conf import settings
from django.db.models import Q

from images.models import Image, UploadImage, GenerateImage
from images.serializers import UploadFileForm, StyleImageSerializer, UpdateStyleImageSerializer, ConvertImageSerializer, \
    TrainingModeSerializer
from rpc import rpc_interface
from utils.api import APIView, check
from utils.constants.account import UserTypeEnum
from utils.constants.images import ImageTypeEnum
from utils.shortcuts import rand_str, save_file, delete_file


class StyleImageAPI(APIView):
    @check([UserTypeEnum.super_admin])
    def get(self, request):
        style_images = Image.objects.filter(image_type=ImageTypeEnum.style_image)
        return self.success(StyleImageSerializer(style_images, many=True).data)

    @check([UserTypeEnum.super_admin], serializer=UpdateStyleImageSerializer)
    def put(self, request):
        data = request.data
        image_id = data['id']
        update_name = data['update_name']
        try:
            image = Image.objects.get(id=image_id)
            image.upload_name = update_name
            image.save()
        except Image.DoesNotExist:
            return self.error('图片不存在')
        return self.success()

    @check([UserTypeEnum.super_admin])
    def delete(self, request):
        image_id = request.data.get('id')
        try:
            image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            return self.error('图片不存在')
        
        delete_file(image.now_name, path=settings.STYLE_IMAGE_PATH)
        image.delete()

        return self.success()


class UploadStyleImageAPI(APIView):
    request_parsers = ()

    @check([UserTypeEnum.super_admin])
    def post(self, request):
        upload_file_form = UploadFileForm(request.POST, request.FILES)
        if not upload_file_form.is_valid():
            return self.error(msg='文件上传失败')

        file = request.FILES['file']
        upload_file_name = file.name
        upload_name = upload_file_name.split('.')[0]
        now_name = rand_str(length=16)

        save_file(file, now_name, path=settings.STYLE_IMAGE_PATH)
        Image.objects.create(upload_name=upload_name, now_name=now_name, image_type=ImageTypeEnum.style_image)
        return self.success()


class UploadOriginImageAPI(APIView):
    request_parsers = ()

    @check([UserTypeEnum.super_admin])
    def post(self, request):
        upload_file_form = UploadFileForm(request.POST, request.FILES)
        if not upload_file_form.is_valid():
            return self.error(msg='文件上传失败')

        file = request.FILES['file']
        upload_file_name = file.name
        upload_name = upload_file_name.split('.')[0]
        now_name = rand_str(length=16)

        save_file(file, now_name, path=settings.ORIGINAL_IMAGE_PATH)
        image = Image.objects.create(upload_name=upload_name, now_name=now_name, image_type=ImageTypeEnum.original_image)
        return self.success({'origin_image_path': 'original_image/' + image.now_name, 'name': image.now_name})


class ConvertImageAPI(APIView):
    @check('__all__', serializer=ConvertImageSerializer)
    def post(self, request):
        data = request.data
        origin_image = data['origin_image']
        style_image_ids = data['style_images']
        style_images = Image.objects.filter(image_type=ImageTypeEnum.style_image).\
            filter(reduce(or_, [Q(id=id) for id in style_image_ids])).values_list('now_name', flat=True)
        member = 1 / len(style_images)
        weight = {}
        for i in style_images:
            weight[i] = member
        print(weight)
        try:
            resp = rpc_interface.convert_image(origin_image, weight)
        except grpc._channel._Rendezvous:
            return self.error('Image conversion failed')

        Image.objects.create(now_name=resp, image_type=ImageTypeEnum.generate_image)
        return self.success({'generate_image': 'generate_image/' + resp})


class TrainingModeAPI(APIView):
    @check([UserTypeEnum.super_admin], serializer=TrainingModeSerializer)
    def post(self, request):
        operation = request.data['operation']
        print(operation)
        try:
            resp = rpc_interface.training_mode(operation)
        except grpc._channel._Rendezvous:
            return self.error('operation failed')
        if resp.status is not True:
            return self.error('operation failed')
        print(resp)
        return self.success({'status': resp.message})


class UploadImageAPI(APIView):
    request_parsers = ()

    @check([UserTypeEnum.super_admin])
    def post(self, request):
        upload_file_form = UploadFileForm(request.POST, request.FILES)
        if not upload_file_form.is_valid():
            return self.error(msg='文件上传失败')

        file = request.FILES['file']
        upload_file_name = file.name
        upload_name = upload_file_name.split('.')[0]
        now_name = rand_str(length=16)

        save_file(file, now_name, path=settings.UPLOAD_IMAGE_PATH)
        image = UploadImage.objects.create(upload_name=upload_name, now_name=now_name)
        data = {
            'id': image.id,
            'name': image.upload_name,
            'path': f'generate_image/{image.now_name}',
            'create_time': image.create_time
        }
        return self.success(data)


class AnimeImageAPI(APIView):
    @check('__all__', serializer=ConvertImageSerializer)
    def post(self, request):
        data = request.data
        image_id = data['image_id']
        try:
            image = UploadImage.objects.get(id=image_id)
        except UploadImage.DoesNotExist:
            return self.error('图片不存在')

        try:
            image_name = rpc_interface.convert_anime_style(image.now_name)
        except grpc._channel._Rendezvous:
            return self.error('图片转换失败')

        GenerateImage.objects.create(now_name=image_name)
        return self.success(resp.path)
