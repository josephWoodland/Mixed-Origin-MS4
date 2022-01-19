from django.urls import path
from . import views

urlpatterns = [
    path("partners/", views.partners, name="partners"),
    path("partner-profile/<str:pk>", views.partner_profile, name="partner-profile"),
    path("partner-products/<str:pk>", views.partner_products, name="partner-products"),
]
