from django.urls import path
from . import views

urlpatterns = [
    path("add-product/", views.addProduct, name="add-product"),
]
