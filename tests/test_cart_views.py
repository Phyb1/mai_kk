import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_cart_add_redirects_and_stores_item(client, product):
    url = reverse("cart:cart_add", kwargs={"product_id": product.id})
    response = client.post(url, {"quantity": 2})
    assert response.status_code == 302
    session = client.session
    assert session["cart"][str(product.id)]["quantity"] == 2


def test_cart_add_rejects_out_of_stock(client, out_of_stock_product):
    url = reverse("cart:cart_add", kwargs={"product_id": out_of_stock_product.id})
    response = client.post(url, {"quantity": 1})
    assert response.status_code == 404


def test_cart_detail_generates_whatsapp_link(client, product, settings):
    settings.WHATSAPP_ORDER_NUMBER = "263771234567"
    add_url = reverse("cart:cart_add", kwargs={"product_id": product.id})
    client.post(add_url, {"quantity": 1})

    response = client.get(reverse("cart:cart_detail"))
    assert response.status_code == 200
    link = response.context["whatsapp_link"]
    assert link.startswith("https://wa.me/263771234567?text=")
    assert "Floral" in link or "Floral%20" in link


def test_cart_detail_empty_has_no_whatsapp_link(client):
    response = client.get(reverse("cart:cart_detail"))
    assert response.context["whatsapp_link"] is None


def test_cart_remove(client, product):
    add_url = reverse("cart:cart_add", kwargs={"product_id": product.id})
    client.post(add_url, {"quantity": 1})

    remove_url = reverse("cart:cart_remove", kwargs={"product_id": product.id})
    response = client.post(remove_url)
    assert response.status_code == 302
    assert client.session["cart"] == {}
