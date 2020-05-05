from . import Choices


class UserTypeEnum(Choices):
    super_admin = 'super_admin'
    general_manager = 'general_manager'
    normal_user = 'normal_user'
