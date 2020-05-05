from rest_framework import serializers
from django import forms

from images.models import Image
from utils.constants.rpc import TrainingModeTypeEnum


class UploadFileForm(forms.Form):
    file = forms.FileField()


class StyleImageSerializer(serializers.ModelSerializer):
    now_name = serializers.SerializerMethodField()

    def get_now_name(self, obj):
        now_name = '/style_image/' + obj.now_name
        return now_name

    class Meta:
        model = Image
        fields = ('id', 'upload_name', 'now_name', 'image_type', 'create_time')


class UpdateStyleImageSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    update_name = serializers.CharField(max_length=100)


class ConvertImageSerializer(serializers.Serializer):
    origin_image = serializers.CharField()
    style_images = serializers.ListField(child=serializers.CharField(), allow_empty=False)


class TrainingModeSerializer(serializers.Serializer):
    operation = serializers.ChoiceField(choices=TrainingModeTypeEnum.choices())
