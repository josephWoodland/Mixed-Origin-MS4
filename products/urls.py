from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.products, name="products"),
    path("products/<str:tag>", views.product_tags, name="product_tags"),
    path("add-product/<str:pk>", views.add_product, name="add-product"),
    path("view-product/<str:pk>", views.view_product, name="view-product"),
    path("edit-product/<str:pk>", views.edit_product, name="edit-product"),
    path("delete-product/<str:pk>", views.delete_product, name="delete-product"),
    path("product-list/<str:pk>", views.product_list, name="product-list"),
]
