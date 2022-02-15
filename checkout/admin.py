from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.


class OrderItemAdmin(admin.TabularInline):
    """Admin settings for the OrderItem class"""

    model = OrderItem
    list_display = ("product", "order")
    list_display_link = ("product", "order")
    readonly_fields = ("item_total",)


class OrderAdmin(admin.ModelAdmin):
    """Admin settings for the Order class"""

    inlines = (OrderItemAdmin,)

    readonly_fields = (
        "delivery_costs",
        "sub_total",
        "grand_total",
        "created",
    )

    list_display = (
        "full_name",
        "created",
        "email",
        "postcode",
    )

    list_display_links = (
        "email",
        "created",
    )

    search_fields = (
        "full_name",
        "email",
        "postcode",
        "created",
    )

    ordering = ("-created",)


admin.site.register(Order, OrderAdmin)
