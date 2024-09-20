from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/airport/", include("core.urls")),
    path("api/user/", include("user.urls")),
    path("api/doc/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/doc/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
] + debug_toolbar_urls()
