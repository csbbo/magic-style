from django.conf import settings
from django.urls import path

from utils.api import APIView

import inspect
import re
import importlib
import logging


logger = logging.getLogger(__name__)


class ExportAPIEntryPoints:
    @classmethod
    def _is_export_api_view(cls, obj):
        return inspect.isclass(obj) and issubclass(obj, APIView) and re.match(r"^.+API$", obj.__name__)

    @classmethod
    def export_urlpatterns(cls):
        _urlpatterns = []
        for item in settings.INSTALLED_APPS:
            try:
                views = importlib.import_module(item+".views")
            except ModuleNotFoundError:
                continue
            views = inspect.getmembers(views,cls._is_export_api_view)
            for name, _class in views:
                url = f"api/{name}"
                _urlpatterns.append(path(url, _class.as_view(), name=name))
                logger.info(f"Detected {name}, url:{url}")
        return _urlpatterns


urlpatterns = ExportAPIEntryPoints.export_urlpatterns()

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
