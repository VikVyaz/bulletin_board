from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.http import HttpResponse

schema_view = get_schema_view(
    openapi.Info(
        title="DRF cluster API project",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="nightronin@yandex.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
)


def health(request):
    return HttpResponse("ok")


urlpatterns = [
    path('health/', health),

    path("admin/", admin.site.urls),
    path("board/", include("board.urls", namespace="board")),
    path("users/", include("users.urls", namespace="users")),
    path("front/", include("front.urls", namespace='front')),

    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
