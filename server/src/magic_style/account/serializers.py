from rest_framework import serializers

from account.models import User
from utils.constants.account import UserTypeEnum


class UserLoginSerializer(serializers.Serializer):
    loginname = serializers.CharField()
    password = serializers.CharField(max_length=32)


class RegistSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128)
    phone_number = serializers.CharField(required=False, max_length=11, min_length=11)
    email = serializers.EmailField(required=False)
    avatar_path = serializers.CharField(required=False)
    remark = serializers.CharField(required=False)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password", "old_password")


class AddUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128)
    user_type = serializers.ChoiceField(choices=UserTypeEnum.choices())
    phone_number = serializers.CharField(required=False, max_length=11, min_length=11)
    email = serializers.EmailField(required=False)
    avatar_path = serializers.CharField(required=False)
    remark = serializers.CharField(required=False)


class UpdateUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(required=False, max_length=64)
    password = serializers.CharField(required=False, max_length=128)
    user_type = serializers.ChoiceField(choices=UserTypeEnum.choices())
    phone_number = serializers.CharField(required=False, max_length=11, min_length=11)
    email = serializers.EmailField(required=False)
    avatar_path = serializers.CharField(required=False)
    remark = serializers.CharField(required=False)
