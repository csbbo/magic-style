from utils.tests import APITestCase


class PlatformInfoAPITest(APITestCase):
    def setUp(self):
        self.url = self.get_url("PlatformInfoAPI")
        self.user = self.create_user()

    def test_get_platform_info(self):
        resp = self.client.get(self.url)
        self.assertSuccess(resp)
