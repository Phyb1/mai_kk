from django.views.generic import TemplateView

from apps.catalog.models import Category, Product


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_products"] = Product.objects.filter(
            in_stock=True, is_featured=True
        ).select_related("category")[:8]
        context["categories"] = Category.objects.all()
        return context


class AboutView(TemplateView):
    template_name = "core/about.html"
