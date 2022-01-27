from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("checkout_success/<str:pk>",
         views.checkout_success, name="checkout_success"),
    path("wh/", webhook, name="webhook"),
]
