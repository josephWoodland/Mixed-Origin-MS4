from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.products, name="products"),
    path("add-product/<str:pk>", views.addProduct, name="add-product"),
    path("view-product/<str:pk>", views.viewProduct, name="view-product"),
    path("edit-product/<str:pk>", views.editProduct, name="edit-product"),
    path("delete-product/<str:pk>", views.deleteProduct, name="delete-product"),
    path("product-list/<str:pk>", views.productList, name="product-list"),
]
