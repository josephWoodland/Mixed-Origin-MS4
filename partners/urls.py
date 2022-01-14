from django.urls import path
from . import views

urlpatterns = [
    path("partners/", views.partners, name="partners"),
    path("partner-profile/<str:pk>", views.partnerProfile, name="partner-profile"),
]
