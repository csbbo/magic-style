import os

from django.conf import settings

from utils.shortcuts import create_random_image, delete_file
from utils.tests import APITestCase


class StyleImageAPITest(APITestCase):
    def setUp(self):
        self.url = self.get_url("StyleImageAPI")
        self.user = self.create_user()

        self.file_path_exist = True
        self.filename = 'style_image_test.png'
        self.file_path = settings.STYLE_IMAGE_PATH

    def test_style_image_api(self):
        if not os.path.exists(self.file_path):
            self.file_path_exist = False
            os.makedirs(self.file_path)
        create_random_image(self.filename, self.file_path)

        with open(os.path.join(self.file_path, self.filename), 'rb') as fd:
            resp = self.client.post(self.get_url('UploadStyleImageAPI'), data={"file": fd}, format='multipart')
        self.assertSuccess(resp)

        resp = self.client.get(self.url)
        self.assertSuccess(resp)
        uuid = resp.data['data'][0]['id']

        resp = self.client.delete(self.url, data={'id': uuid})
        self.assertSuccess(resp)

        os.remove(os.path.join(self.file_path, self.filename))
        if os.path.exists(self.file_path) and self.file_path_exist is False:
            os.removedirs(self.file_path)


class UploadOriginImageAPITest(APITestCase):
    def setUp(self):
        self.url = self.get_url("UploadOriginImageAPI")
        self.user = self.create_user()

        self.file_path_exist = True
        self.filename = 'origin_image_test.png'
        self.file_path = settings.ORIGINAL_IMAGE_PATH

    def test_origin_image_upload(self):
        if not os.path.exists(self.file_path):
            self.file_path_exist = False
            os.makedirs(self.file_path)
        create_random_image(self.filename, self.file_path)

        with open(os.path.join(self.file_path, self.filename), 'rb') as fd:
            resp = self.client.post(self.url, data={"file": fd}, format='multipart')
        self.assertSuccess(resp)

        now_name = resp.data['data']['origin_image_path'].split('/')[-1]
        os.remove(os.path.join(self.file_path, now_name))

        os.remove(os.path.join(self.file_path, self.filename))
        if os.path.exists(self.file_path) and self.file_path_exist is False:
            os.removedirs(self.file_path)
