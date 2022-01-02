from django.urls import path
from . import views

urlpatterns = [
    path("add-product/", views.addProduct, name="add-product"),
    path("view-product/<str:pk>", views.viewProduct, name="view-product"),
]
