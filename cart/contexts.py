from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def cart_contents(request):

    cart_items = []
    total = 0
    product_count = 0
    free_delivery_threshold = settings.FREE_STANDARD_DELIVERY_THRESHOLD
    amount_to_free_standard_delivery = 0

    cart = request.session.get("cart", {})

    for item_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        total += quantity * product.price
        product_count += quantity

        cart_items.append(
            {
                "item_id": item_id,
                "quantity": quantity,
                "product": product,
                "product_count": product_count,
            }
        )

    # Show how much to spend to get free standard delivery 

    if total < free_delivery_threshold:
        delivery = 10
        free_delivery = False
        amount_to_free_standard_delivery = free_delivery_threshold - total
    else:
        delivery = 0
        free_delivery = True

    grand_total = delivery + total

    context = {
        "cart_items": cart_items,
        "total": total,
        "product_count": product_count,
        "free_delivery": free_delivery,
        "free_delivery_threshold": free_delivery_threshold,
        "grand_total": grand_total,
        "amount_to_free_standard_delivery": amount_to_free_standard_delivery,
    }

    return context
