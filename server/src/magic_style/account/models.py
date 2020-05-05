from django.contrib.auth.models import AbstractBaseUser, UserManager as AbstractUserManager
from django.contrib.postgres.fields import ArrayField
from django.db import models

from utils.constants.account import UserTypeEnum


class UserManager(AbstractUserManager):
    use_in_migrations = True

    def get_by_natural_key(self, username):
        return self.get(username=username)

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, password, email=None, **extra_fields):
        extra_fields.setdefault('user_type', UserTypeEnum.super_admin)
        if extra_fields.get('user_type') != UserTypeEnum.super_admin:
            raise ValueError('Superuser must have user_type=%s.' % UserTypeEnum.super_admin)
        return self._create_user(username, password, email, **extra_fields)


class User(AbstractBaseUser):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")
    username = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=128)
    old_password = ArrayField(models.CharField(null=True, blank=True, max_length=128), default=list)
    user_type = models.CharField(default=UserTypeEnum.normal_user, max_length=32)
    phone_number = models.CharField(null=True, max_length=11, unique=True)
    email = models.TextField(null=True, unique=True)
    avatar_path = models.TextField(null=True)
    remark = models.TextField(null=True)

    create_time = models.DateTimeField(auto_now_add=True)
    last_login_time = models.DateTimeField(null=True)
    last_update_time = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'

    object = UserManager()

    class Meta:
        db_table = 'user'
        ordering = ['id']
