from django.db.models import Q
from django.utils import timezone
from django.contrib import auth
from django.db import transaction

from account.models import User
from account.serializers import UserLoginSerializer, RegistSerializer, UserSerializer, AddUserSerializer, \
    UpdateUserSerializer
from utils.api import APIView, check
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from utils.constants.account import UserTypeEnum


class LoginAPI(APIView):
    @check(login_required=False, serializer=UserLoginSerializer)
    def post(self, request):
        loginname = request.data['loginname']
        password = request.data['password']

        user = User.object.filter(Q(username=loginname) | Q(phone_number=loginname) | Q(email=loginname))
        if not user.exists():
            return self.error("用户不存在")

        user = user.first()
        if not user.check_password(password):
            return self.error("密码错误")

        with transaction.atomic():
            auth.login(request=request, user=user)
            user.last_login_time = timezone.now()
            user.save()
        return self.success()


class LogoutAPI(APIView):
    @check('__all__', login_required=True)
    def post(self, request):
        with transaction.atomic():
            auth.logout(request=request)
        return self.success()


class RegistAPI(APIView):
    @check(login_required=False, serializer=RegistSerializer)
    def post(self, request):
        data = request.data
        password = data['password']
        del data['password']

        if User.object.filter(username=data['username']).exists():
            return self.error("用户名已存在")
        if data.get('phone_number') and User.object.filter(phone_number=data['phone_number']).exists():
            return self.error("该手机号已经被注册")
        if data.get('email') and User.object.filter(email=data['email']).exists():
            return self.error("该邮箱已经被注册")

        with transaction.atomic():
            user = User.object.create(**data)
            user.set_password(password)
            user.save()

        auth.login(request=request, user=user)
        return self.success()


class CSRFTokenAPI(APIView):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return self.success()


class LoginStatusAPI(APIView):
    @check(permission='__all__', login_required=True)
    def get(self, request):
        return self.success()


class UserIdentityAPI(APIView):
    @check('__all__')
    def get(self, request):
        return self.success({'user_type': request.user.user_type})


class UserTypeEnumAPI(APIView):
    @check('__all__')
    def get(self, request):
        data = [
            {'value': UserTypeEnum.normal_user, 'name': '普通用户'},
            {'value': UserTypeEnum.general_manager, 'name': '管理员'},
        ]
        return self.success(data)


class UserAPI(APIView):
    @check('__all__')
    def get(self, request):
        data = request.data
        user_id = data.get('user_id')
        user_type = data.get('user_type')
        if bool(user_id):
            try:
                user = User.object.get(id=user_id)
            except User.DoesNotExist:
                return self.error('用户不存在!')
            return self.success(UserSerializer(user).data)

        if request.user.user_type != UserTypeEnum.super_admin:
            return self.error('没有获取所有用户信息权限')

        users = User.object.exclude(user_type=UserTypeEnum.super_admin)
        if bool(user_type):
            users = users.filter(user_type=user_type)

        return self.success(UserSerializer(users, many=True).data)

    @check([UserTypeEnum.super_admin, UserTypeEnum.general_manager], serializer=AddUserSerializer)
    def post(self, request):
        data = request.data
        password = data['password']
        del data['password']

        if User.object.filter(username=data['username']).exists():
            return self.error("用户名已存在")
        if data.get('phone_number') and User.object.filter(phone_number=data['phone_number']).exists():
            return self.error("该手机号已经被注册")
        if data.get('email') and User.object.filter(email=data['email']).exists():
            return self.error("该邮箱已经被注册")

        with transaction.atomic():
            user = User.object.create(**data)
            user.set_password(password)
            user.save()

        return self.success()

    @check([UserTypeEnum.super_admin], serializer=UpdateUserSerializer)
    def put(self, request):
        data = request.data
        password = data.get('password')

        try:
            user = User.object.get(id=data['id'])
            if bool(password):
                user.set_password(password)
                del data['password']
            user.save()
        except User.DoesNotExist:
            return self.error('用户不存在')

        if User.object.filter(~Q(id=data['id']), username=data['username']).exists():
            return self.error("用户名已存在")
        if data.get('phone_number') and User.object.filter(~Q(id=data['id']), phone_number=data['phone_number']).exists():
            return self.error("该手机号已经被注册")
        if data.get('email') and User.object.filter(~Q(id=data['id']), email=data['email']).exists():
            return self.error("该邮箱已经被注册")

        with transaction.atomic():
            User.object.filter(id=data['id']).update(**data)

        return self.success()

    @check([UserTypeEnum.super_admin])
    def delete(self, request):
        data = request.data
        user_ids = data.get('user_ids')
        if not bool(user_ids):
            return self.error('请指定要删除的用户ID')

        users = User.object.filter(id__in=user_ids)
        if not users.exists():
            return self.error('用户不存在')

        users.delete()
        return self.success()
