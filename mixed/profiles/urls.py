from django.urls import path
from . import views

urlpatterns = [
    path("profile/", views.userProfile, name="profile"),
    path("edit_profile/", views.editProfile, name="edit_profile"),
    path("delete_profile/", views.deleteProfile, name="delete_profile"),
    path("wallet/<str:pk>", views.userWallet, name="wallet"),
]
