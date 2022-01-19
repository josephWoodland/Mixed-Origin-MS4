from django.urls import path
from . import views

urlpatterns = [
    path("cart", views.cart, name="cart"),
    path("cart/<item_id>", views.add_to_cart, name="add-to-cart"),
]
