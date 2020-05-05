from account.models import User
from utils.constants.account import UserTypeEnum
from utils.tests import APITestCase


class LoginAPITest(APITestCase):
    def setUp(self):
        self.url = self.get_url("LoginAPI")
        self.user = self.create_user(login=False)

    def test_login_success(self):
        resp = self.client.post(self.url, data={"loginname": self.TEST_USERNAME, "password": self.TEST_PASSWORD})
        self.assertSuccess(response=resp)

        resp = self.client.post(self.url, data={"loginname": "test@email.com", "password": self.TEST_PASSWORD})
        self.assertFailed(response=resp)


class RegistAPITest(APITestCase):
    def setUp(self):
        self.url = self.get_url("RegistAPI")

    def test_regist_success(self):
        data = {'username': 'xiaoming', 'password': '123456'}
        resp = self.client.post(self.url, data=data)
        self.assertSuccess(resp)


class UserAPITest(APITestCase):
    def setUp(self):
        self.url = self.get_url("UserAPI")
        self.user = self.create_user()
        data1 = {
            'id': 17,
            'username': 'testUser1',
            'password': '1234567890',
            'user_type': UserTypeEnum.normal_user,
            'phone_number': '12345678901',
            'email': 'testUser1@gmail.com',
            'remark': 'some thing to say 1'
        }
        data2 = {
            'id': 18,
            'username': 'testUser2',
            'password': '1234567890',
            'user_type': UserTypeEnum.normal_user,
            'phone_number': '12345678902',
            'email': 'testUser2@gmail.com',
            'remark': 'some thing to say 2'
        }

        User.object.create(**data1)
        User.object.create(**data2)

    def test_get_one_user(self):
        resp = self.client.get(self.url, data={'user_id': 18})
        self.assertSuccess(resp)

    def test_get_multi_user(self):
        resp = self.client.get(self.url, data={'user_type': UserTypeEnum.general_manager})
        self.assertSuccess(resp)

    def test_get_all_user(self):
        resp = self.client.get(self.url)
        self.assertSuccess(resp)

    def test_add_user(self):
        data = {
            'username': 'testUser3',
            'password': '1234567890',
            'user_type': UserTypeEnum.normal_user,
            'phone_number': '12345678903',
            'email': 'testUser3@gmail.com',
            'remark': 'some thing to say 3'
        }
        resp = self.client.post(self.url, data=data)
        self.assertSuccess(resp)

    def test_update_user(self):
        data = {
            'id': 18,
            'username': 'testUser4',
            'password': '1234567890',
            'user_type': UserTypeEnum.normal_user,
            'phone_number': '12345678904',
            'email': 'testUser4@gmail.com',
            'remark': 'some thing to say 3'
        }
        resp = self.client.put(self.url, data=data)
        self.assertSuccess(resp)

    def test_delete_user(self):
        resp = self.client.delete(self.url, data={'user_ids': [18, 17]})
        self.assertSuccess(resp)


class UserTypeEnumAPITest(APITestCase):
    def setUp(self):
        self.url = self.get_url("UserTypeEnumAPI")
        self.user = self.create_user()

    def test_get_user_type_enums(self):
        resp = self.client.get(self.url)
        self.assertSuccess(resp)
