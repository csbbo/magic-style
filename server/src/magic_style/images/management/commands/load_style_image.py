import logging
import os
import shutil
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand

from images.models import StyleImage
from utils.shortcuts import rand_str

logger = logging.getLogger('load_style_image')


def remove_temp_dir(dir_path):
    shutil.rmtree(dir_path)


def validate_dir(dir_path):
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        return True
    return False


class Command(BaseCommand):
    help = "import the package which contain the style images"

    def add_arguments(self, parser):
        parser.add_argument("file_path", nargs="?", type=str, help="The package full path")

    def handle(self, *args, **options):
        file_path = options['file_path']

        if os.path.exists(settings.IMPORT_TEMP_FILE_PATH) is not True:
            os.mkdir(settings.IMPORT_TEMP_FILE_PATH)

        subprocess.check_call(['unzip', file_path, '-d', settings.IMPORT_TEMP_FILE_PATH])

        if validate_dir(os.path.join(settings.IMPORT_TEMP_FILE_PATH, 'style_image')):
            path = os.path.join(settings.IMPORT_TEMP_FILE_PATH, 'style_image')
            for name in os.listdir(path):
                if not name.split('.')[1] in ['.jpg', '.png', '.jpeg']:
                    continue
                name = name.split('.')[0]
                now_name = rand_str() + '.png'
                image_path = os.path.join(settings.STYLE_IMAGE_PATH, now_name)
                with open(os.path.join(path, name), 'r') as upload_f:
                    with open(image_path, 'wb+') as now_f:
                        now_f.write(upload_f)

                StyleImage.obejects.create(upload_name=name, image_path=image_path)

        remove_temp_dir(settings.IMPORT_TEMP_FILE_PATH)
        logger.info(f"Style images has been add success")
