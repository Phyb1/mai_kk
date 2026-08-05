from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve as static_serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cart/", include("apps.cart.urls")),
    path("", include("apps.catalog.urls")),
    path("", include("apps.core.urls")),
]

# Serve static and media explicitly for Passenger sub-URI deployments
# This works even when STATIC_URL = '/onspot/static/' because Django matches
# against PATH_INFO after SCRIPT_NAME is stripped by Passenger
urlpatterns += [
    re_path(r"^static/(?P<path>.*)$", static_serve, {"document_root": settings.STATIC_ROOT}),
    re_path(r"^media/(?P<path>.*)$", static_serve, {"document_root": settings.MEDIA_ROOT}),
]

# Keep this for DEBUG if you also want runserver to work with /media/
if settings.DEBUG:
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", static_serve, {"document_root": settings.MEDIA_ROOT}),
    ]
