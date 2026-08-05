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

# Explicit static/media routes — needed because this app is deployed under
# a Passenger sub-URI. Passenger strips that prefix before Django sees the
# request, so WhiteNoise's own "does path start with STATIC_URL" check can
# never match once STATIC_URL includes the sub-path (needed for correct
# hrefs). Django's URL resolver handles the stripped path correctly.
urlpatterns += [
    re_path(r"^static/(?P<path>.*)$", static_serve, {"document_root": settings.STATIC_ROOT}),
    re_path(r"^media/(?P<path>.*)$", static_serve, {"document_root": settings.MEDIA_ROOT}),
]
