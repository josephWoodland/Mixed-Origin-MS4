from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    list_display = ("product", "order")
    list_display_link = ("product", "order")
    readonly_fields = ("item_total",)


class OrderAdmin(admin.ModelAdmin):

    inlines = (OrderItemAdmin,)

    readonly_fields = (
        "id",
        "delivery_costs",
        "sub_total",
        "grand_total",
        "created",
    )

    list_display = (
        "id",
        "full_name",
        "created",
        "email",
        "postcode",
    )

    list_display_links = (
        "id",
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
