import pytest

pytestmark = pytest.mark.django_db


def test_category_slug_auto_generated(category):
    assert category.slug == "women"


def test_product_slug_auto_generated(product):
    assert product.slug == "floral-summer-dress"


def test_product_get_absolute_url(product):
    assert product.get_absolute_url() == f"/shop/item/{product.slug}/"


def test_category_get_absolute_url(category):
    assert category.get_absolute_url() == f"/shop/category/{category.slug}/"


def test_product_display_image_falls_back_to_placeholder(product):
    assert product.image.name in (None, "")
    assert product.display_image_url == "/static/images/placeholders/product-placeholder.png"


def test_category_str_and_ordering(category, out_of_stock_category):
    from apps.catalog.models import Category

    names = list(Category.objects.values_list("name", flat=True))
    assert names == ["Women", "Kids"]  # ordered by `order` field
    assert str(category) == "Women"
