import copy
import json

from django.test.testcases import TestCase
from django.urls import reverse

from account.models import User
from utils.shortcuts import MyJSONEncoder
from .constants.account import UserTypeEnum
from rest_framework.test import APIClient


class DocumentAPIClient(APIClient):
    def _request(self, method, *args, **kwargs):
        resp = getattr(super(), method)(*args, **kwargs)
        return resp

    def get(self, *args, **kwargs):
        return self._request("get", *args, **kwargs)

    def post(self, *args, **kwargs):
        return self._request("post", *args, **kwargs)

    def put(self, *args, **kwargs):
        return self._request("put", *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self._request("delete", *args, **kwargs)


class APITestCase(TestCase):
    client_class = DocumentAPIClient
    TEST_USERNAME = "super_admin"
    TEST_PASSWORD = "super_admin"

    @classmethod
    def setUpTestData(cls):
        print(f"\n\033[32m[Test Class: {cls.__name__}]\033[0m")

    def create_user(self, username=TEST_USERNAME, password=TEST_PASSWORD,
                    login=True, user_type=UserTypeEnum.super_admin):
        user = User.object.create(username=username)
        user.set_password(password)
        user.user_type = user_type
        user.save()
        if login:
            self.login(username, password)
        return user

    def login(self, username, password):
        self.assertIsNotNone(self.client.login(username=username, password=password), "login failed")

    def get_url(self, url_name):
        return reverse(url_name)

    def assertSuccess(self, response):
        self.assertIsNone(response.data["err"],
                          f"\n\033[31m[RESPONSE]\033[0m {json.dumps(response.data, ensure_ascii=False, cls=MyJSONEncoder)}")
        return response.data["data"]

    def assertFailed(self, response, err=None, msg=None, msg__contains=None):
        self.assertIsNotNone(response.data["err"],
                             f"\n\033[31m[RESPONSE]\033[0m {json.dumps(response.data, ensure_ascii=False, cls=MyJSONEncoder)}")
        if err:
            self.assertEqual(response.data["err"], err)
        if msg:
            self.assertEqual(response.data["msg"], msg)
        if msg__contains:
            if isinstance(msg__contains, str):
                self.assertIn(msg__contains, response.data["msg"])
            elif isinstance(msg__contains, list):
                for item in msg__contains:
                    self.assertIn(item, response.data["msg"])
            else:
                raise ValueError()
        return response.data

    def assertDictContains(self, subset, dict_data):
        for k in subset.keys():
            self.assertEqual(subset[k], dict_data[k])

    def deepcopy(self, data):
        return copy.deepcopy(data)
