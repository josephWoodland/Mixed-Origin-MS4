from django.urls import path
from . import views

urlpatterns = [
    path("cart", views.cart, name="cart"),
    path("cart/<item_id>", views.add_to_cart, name="add-to-cart"),
    path("update-cart/<str:pk>", views.update_cart, name="update-cart"),
    path("delete-cart-item/<str:pk>", views.delete_cart_item, name="delete-cart-item"),
]
