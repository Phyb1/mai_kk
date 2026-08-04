from urllib.parse import quote

from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.catalog.models import Product

from .cart import Cart


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, in_stock=True)
    quantity = int(request.POST.get("quantity", 1))
    cart.add(product=product, quantity=max(quantity, 1))
    messages.success(request, f"Added {product.name} to your bag.")
    return redirect(request.POST.get("next", "cart:cart_detail"))


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))
    cart.update_quantity(product, quantity)
    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f"Removed {product.name} from your bag.")
    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    whatsapp_link = build_whatsapp_order_link(cart) if len(cart) else None
    return render(
        request,
        "cart/cart_detail.html",
        {"cart": cart, "whatsapp_link": whatsapp_link},
    )


def build_whatsapp_order_link(cart):
    lines = ["Hi Mimie's Closet, I'd like to order:"]
    for item in cart:
        lines.append(
            f"- {item['product'].name} x{item['quantity']} "
            f"(${item['subtotal']:.2f})"
        )
    lines.append(f"Total: ${cart.get_total_price():.2f}")
    message = "\n".join(lines)
    number = settings.WHATSAPP_ORDER_NUMBER
    return f"https://wa.me/{number}?text={quote(message)}"
