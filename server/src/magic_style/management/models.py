from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext

from account.models import User
from utils.shortcuts import MyJSONEncoder


class AuditLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField(null=True)
    log_type = models.TextField()
    explain = models.TextField()
    raw_data = JSONField(encoder=MyJSONEncoder)
    create_time = models.DateTimeField(auto_now_add=True)

    @property
    def username(self):
        if not self.user_id:
            return gettext("Anonymous User")
        try:
            return User.objects.only("username").get(id=self.user_id).username
        except User.DoesNotExist:
            return gettext("Anonymous User")

    class Meta:
        ordering = ("-id",)
