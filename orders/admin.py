from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'total_amount',
        'status',
        'created_at'
    )

    list_filter = ('status',)

    search_fields = (
        'user__username',
        'phone'
    )

    list_editable = ('status',)

    inlines = [OrderItemInline]


admin.site.register(OrderItem)