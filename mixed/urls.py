from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("", include("home.urls")),
    path("admin/", admin.site.urls),
    path("product/", include("products.urls")),
    path("profile/", include("profiles.urls")),
    path("partners/", include("partners.urls")),
    path("cart/", include("cart.urls")),
    path("checkout/", include("checkout.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
