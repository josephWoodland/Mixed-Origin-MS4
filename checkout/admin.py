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
        "tracking_number",
        "order_number",
        "delivery_costs",
        "sub_total",
        "grand_total",
    )

    list_display = (
        "tracking_number",
        "email",
        "created",
        "postcode",
        "full_name",
    )

    list_display_links = (
        "tracking_number",
        "email",
        "created",
    )

    search_fields = (
        "tracking_number",
        "full_name",
        "email",
        "postcode",
        "created",
    )

    ordering = ("-created",)


admin.site.register(Order, OrderAdmin)
