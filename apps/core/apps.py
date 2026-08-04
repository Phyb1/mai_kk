from django.contrib import admin
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"

    def ready(self):
        admin.site.site_header = "Mimie's Closet Admin"
        admin.site.site_title = "Mimie's Closet"
        admin.site.index_title = "Manage catalog"
