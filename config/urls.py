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

# Serve static and media with the /mai_kk/ prefix
# Passenger strips /mai_kk from SCRIPT_NAME, so Django matches this
urlpatterns += [
    re_path(r"^mai_kk/static/(?P<path>.*)$", static_serve, {"document_root": settings.STATIC_ROOT}),
    re_path(r"^mai_kk/media/(?P<path>.*)$", static_serve, {"document_root": settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r"^mai_kk/media/(?P<path>.*)$", static_serve, {"document_root": settings.MEDIA_ROOT}),
    ]
