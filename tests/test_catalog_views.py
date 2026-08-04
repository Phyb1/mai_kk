import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_product_list_shows_in_stock_products(client, product, out_of_stock_product):
    response = client.get(reverse("catalog:product_list"))
    assert response.status_code == 200
    products = response.context["products"]
    assert product in products
    assert out_of_stock_product not in products


def test_category_filter_scopes_to_category(client, product, out_of_stock_category):
    from apps.catalog.models import Product

    other_product = Product.objects.create(
        category=out_of_stock_category, name="Kids Shirt", price="10.00", in_stock=True
    )
    url = reverse("catalog:category_detail", kwargs={"slug": product.category.slug})
    response = client.get(url)
    products = response.context["products"]
    assert product in products
    assert other_product not in products


def test_product_detail_renders(client, product):
    url = reverse("catalog:product_detail", kwargs={"slug": product.slug})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["product"] == product


def test_home_page_lists_featured_products(client, product):
    response = client.get(reverse("core:home"))
    assert response.status_code == 200
    assert product in response.context["featured_products"]
