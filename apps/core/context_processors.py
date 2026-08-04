from django.conf import settings


def site_settings(request):
    return {
        "SITE_NAME": settings.SITE_NAME,
        "WHATSAPP_ORDER_NUMBER": settings.WHATSAPP_ORDER_NUMBER,
    }
