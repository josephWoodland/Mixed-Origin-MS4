from django.urls import path
from . import views

urlpatterns = [
    path("profile/", views.user_profile, name="profile"),
    path("edit-profile/<str:pk>", views.edit_profile, name="edit-profile"),
    path("edit-partner/<str:pk>", views.edit_partner, name="edit-partner"),
    path("delete-profile/<str:pk>", views.delete_profile, name="delete-profile"),
    path("wallet/<str:pk>", views.user_wallet, name="wallet"),
    path("orders/<str:pk>", views.orders, name="orders"),
]
