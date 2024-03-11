from django.contrib import admin
from django.urls import path, include
import user.urls as user_urls
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(openapi.Info(title="輿情產品 API", default_version="v1"))

urlpatterns = [
    path("admin/", admin.site.urls),
    path("docs/", schema_view.with_ui("swagger")),
    path("user/", include(user_urls)),
]
