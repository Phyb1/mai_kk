import pytest

from apps.catalog.models import Category, Product


@pytest.fixture
def category(db):
    return Category.objects.create(name="Women", order=1)


@pytest.fixture
def out_of_stock_category(db):
    return Category.objects.create(name="Kids", order=2)


@pytest.fixture
def product(db, category):
    return Product.objects.create(
        category=category,
        name="Floral Summer Dress",
        price="25.00",
        in_stock=True,
        is_featured=True,
    )


@pytest.fixture
def out_of_stock_product(db, category):
    return Product.objects.create(
        category=category,
        name="Sold Out Jacket",
        price="40.00",
        in_stock=False,
    )
