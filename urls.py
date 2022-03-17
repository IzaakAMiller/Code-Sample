"""
Blast Backend URL Configuration
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views.blast import BlastViewSet
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

router = DefaultRouter()

router.register(r'blast', BlastViewSet, 'blast')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
]

api_info = openapi.Info(
        title="Blast API",
        default_version="1.0",
        description="APIs found in Blast",
    )

schema_view = get_schema_view(
    api_info, public=True, permission_classes=(permissions.AllowAny,)
)

swagger_views = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.with_ui(cache_timeout=0),
        name="schema",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
urlpatterns.extend(swagger_views)
