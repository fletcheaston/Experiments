from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app_blog.urls")),
    path("my-freight-cube/", include("app_my_freight_cube.urls")),
]
