import json
import typing
import functools
import errno
import logging
from urllib.parse import quote

from .shortcuts import MyJSONEncoder, logger
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse, QueryDict
from django.views.generic import View

from management.models import AuditLog

api_request_logger = logging.getLogger("api.request")


class ContentType:
    json_request = "application/json"
    json_response = "application/json;charset=UTF-8"
    url_encoded_request = "application/x-www-form-urlencoded"
    binary_response = "application/octet-stream"


class JSONParser:
    content_type = ContentType.json_request

    @staticmethod
    def parse(body):
        return json.loads(body.decode("utf-8"))


class URLEncodedParser:
    content_type = ContentType.url_encoded_request

    @staticmethod
    def parse(body):
        return QueryDict(body)


class JSONResponse:
    content_type = ContentType.json_response

    @classmethod
    def response(cls, data, status):
        resp = HttpResponse(json.dumps(data, indent=4, cls=MyJSONEncoder),
                            content_type=cls.content_type, status=status)
        resp.data = data
        return resp


class APIError(Exception):
    def __init__(self, msg: str, *, err: str = "error"):
        self.err = err
        self.msg = msg
        super().__init__(err, msg)


class APIView(View):
    request_parsers = (JSONParser, URLEncodedParser)
    response_class = JSONResponse
    support_paginate = False

    def _get_request_data(self):
        if self.request.method != "GET":
            body = self.request.body
            content_type = self.request.META.get("CONTENT_TYPE")
            if not content_type:
                raise ValueError("content_type is required")
            for parser in self.request_parsers:
                if content_type.startswith(parser.content_type):
                    break
            else:
                raise ValueError(f"unknown content_type '{content_type}'")
            if body:
                return parser.parse(body)
            return {}
        return self.request.GET

    def response(self, data: typing.Union[list, dict, int, float, str], *, status: int = 200):
        resp = self.response_class.response(data, status=status)
        resp.support_paginate = self.support_paginate
        return resp

    def success(self, data: typing.Union[list, dict, int, float, str] = None, status: int = 200):
        return self.response({"err": None, "data": data}, status=status)

    def error(self, msg: str, *, err: str = "error", status: int = 200):
        return self.response({"err": err, "msg": msg}, status=status)

    def extract_errors(self, errors, key="field"):
        if isinstance(errors, dict):
            if not errors:
                return key, "Invalid field"
            key = list(errors.keys())[0]
            return self.extract_errors(errors.pop(key), key)
        elif isinstance(errors, list):
            return self.extract_errors(errors[0], key)

        return key, errors

    def server_error(self):
        return self.error(err="server-error", msg="服务器错误")

    def object_does_not_exist(self, obj=""):
        if not obj:
            msg = "对象不存在"
        else:
            msg = f"{obj}: 对象不存在"
        return self.error(err="object-not-found", msg=msg)

    def invalid_serializer(self, serializer):
        key, error = self.extract_errors(serializer.errors)
        if key == "non_field_errors":
            msg = error
        else:
            msg = f"{error}"
        return self.error(err=f"invalidfield-{key}", msg=msg)

    def permission_denied(self):
        return self.error(err="permission-denied", msg="访问受限")

    def login_required(self):
        return self.error(err="login-required", msg="需要登录", status=401)

    def failed_to_upload(self):
        return self.error(err="upload-failed", msg="上传文件失败")

    def user_operation_log(self, explain, *, log_type, raw_data: dict = {}):
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        else:
            user_id = None
        return AuditLog.objects.create(user_id=user_id, explain=explain, log_type=str(log_type), raw_data=raw_data)

    def download(self, upload_name, now_name, *, content_type="application/octet-stream"):
        resp = self.success()
        resp["X-Accel-Redirect"] = f"/_/download/{now_name}"
        resp["Content-Disposition"] = f"attachment; filename*=UTF-8''{quote(upload_name)}"
        resp["Content-Type"] = content_type
        return resp

    def preview_pdf(self, upload_name, now_name):
        resp = self.success()
        resp['X-Accel-Redirect'] = f'/_/lesson/pdf/{now_name}'
        resp['Content-Disposition'] = f"inline; filename*=UTF-8''{quote(upload_name)}"
        resp['Content-Type'] = 'application/pdf'
        return resp

    def paginate_data(self, query_set, object_serializer=None, force=False, context=None):
        """
        :param query_set: django model的query set或者其他list like objects
        :param object_serializer: 用来序列化query set, 如果为None, 则直接对query set切片
        :param force: 是否强制翻页
        :param context: 为serializer提供的额外的上下文参数
        :return:
        """
        self.support_paginate = True

        need_paginate = self.request.GET.get("count", None)
        if need_paginate is None:
            if force:
                raise APIError("'count' is required")
            if object_serializer:
                return object_serializer(query_set, many=True).data
            else:
                return query_set
        try:
            limit = int(self.request.GET.get("count", "100"))
        except ValueError:
            limit = 100
        if limit < 0:
            limit = 100
        try:
            offset = int(self.request.GET.get("offset", "0"))
        except ValueError:
            offset = 0
        if offset < 0:
            offset = 0
        results = query_set[offset:offset + limit]
        if object_serializer:
            count = query_set.count() if not isinstance(query_set, list) else len(query_set)
            results = object_serializer(results, many=True, context=context).data if context \
                else object_serializer(results, many=True).data
        else:
            count = len(query_set)
        data = {"items": results,
                "total": count}
        return data

    def dispatch(self, request, *args, **kwargs):
        if self.request_parsers:
            try:
                request.data = self._get_request_data()
                api_request_logger.debug(f"\n\n{request.method} {request.path}\n"
                                         f"User-Agent: {request.META.get('HTTP_USER_AGENT', '')}\n"
                                         f"{request.data}\n")
            except ValueError as e:
                return self.error(err="invalid-request", msg=str(e))

        try:
            return super(APIView, self).dispatch(request, *args, **kwargs)
        except ObjectDoesNotExist as e:
            logger.exception(e)
            return self.object_does_not_exist(str(e).split(" ", maxsplit=1)[0])
        except APIError as e:
            return self.error(err=e.err, msg=e.msg)
        except OSError as e:
            if e.errno == errno.ENOSPC:
                return self.error(msg="硬盘已满，请联系管理员")
        except Exception as e:
            logger.exception(e)
            return self.server_error()


class CSRFExemptAPIView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CSRFExemptAPIView, self).dispatch(request, *args, **kwargs)


class check:
    def __init__(self, permission=None, *, login_required=True, serializer=None, serializer_many=False):
        self.permission = permission
        self.serializer = serializer
        self.serializer_many = serializer_many
        self.login_required = login_required

        if (serializer_many and not serializer) or (permission and not login_required):
            raise ValueError("Invalid check condition")

    def _check_permission(self, request):
        if self.permission is None:
            return False

        if self.permission == '__all__':
            return True

        if request.user.user_type in self.permission:
            return True
        else:
            return False

    def _get_current_user(self, request):
        user = request.user
        if user.is_authenticated:
            return user
        return None

    def __call__(self, fn):
        @functools.wraps(fn)
        def _check(*args, **kwargs):
            func_self = args[0]
            request = args[1]

            if self.login_required:
                user = self._get_current_user(request)
                if not user:
                    return func_self.login_required()
                request.user = user

                if not self._check_permission(request):
                    return func_self.permission_denied()

            if self.serializer:
                s = self.serializer(data=request.data, many=self.serializer_many)
                if s.is_valid():
                    request.data = s.data
                    request.serializer = self.serializer
                else:
                    return func_self.invalid_serializer(s)

            return fn(*args, **kwargs)

        return _check
