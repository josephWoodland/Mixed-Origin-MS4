from django.urls import path
from . import views

urlpatterns = [
    path("profile/", views.userProfile, name="profile"),
    path("edit-profile/<str:pk>", views.editProfile, name="edit-profile"),
    path("edit-partner/<str:pk>", views.editPartner, name="edit-partner"),
    path("delete-profile/<str:pk>", views.deleteProfile, name="delete-profile"),
    path("wallet/<str:pk>", views.userWallet, name="wallet"),
]
