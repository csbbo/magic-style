import logging

from django.core.management.base import BaseCommand

from account.models import User
from utils.constants.account import UserTypeEnum

logger = logging.getLogger('create_superuser')


class Command(BaseCommand):
    help = "create superuser"

    def add_arguments(self, parser):
        parser.add_argument("--username", nargs="?", type=str, help="username")
        parser.add_argument("--password", nargs="?", type=str, help="password")

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']

        if username is None:
            username = 'admin'
        if password is None:
            password = 'admin'

        user = User.object.create(username=username, user_type=UserTypeEnum.super_admin)
        user.set_password(password)
        user.save()

        logger.info("Create superuser success")
