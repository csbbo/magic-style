import psutil
from django.conf import settings

from account.models import User
from images.models import Image
from utils.api import APIView, check
from utils.constants.account import UserTypeEnum
from utils.constants.images import ImageTypeEnum


class PlatformInfoAPI(APIView):
    @check(permission=[UserTypeEnum.super_admin, UserTypeEnum.general_manager])
    def get(self, request):
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        disk = psutil.disk_usage(settings.STYLE_IMAGE_PATH)
        disk_total = round(disk.total / (1024 ** 3), 2)
        disk_use = round((disk.total - disk.free) / (1024 ** 3), 2)

        general_manager_count = User.object.filter(user_type=UserTypeEnum.general_manager).count()
        normal_user_count = User.object.filter(user_type=UserTypeEnum.normal_user).count()
        style_image_count = Image.objects.filter(image_type=ImageTypeEnum.style_image).count()

        data = {
            'cpu_usage': cpu_usage,
            'memory_usage': memory_usage,
            'disk_total': disk_total,
            'disk_use': disk_use,
            'general_manager_count': general_manager_count,
            'normal_user_count': normal_user_count,
            'style_image_count': style_image_count,
        }
        return self.success(data=data)
