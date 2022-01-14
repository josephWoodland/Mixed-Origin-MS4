from django.urls import path
from . import views

urlpatterns = [
    path("partners/", views.partners, name="partners"),
]
