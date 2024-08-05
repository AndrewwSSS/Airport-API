from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/airport/", include("core.urls")),
    path("api/user/", include("user.urls")),
]
