from django.contrib import admin
from .models import Order, PromoCode


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'salesman_name',
        'usage_count',
        'is_active',
        'created_at'
    )
    search_fields = ('code', 'salesman_name')
    list_filter = ('is_active',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'total_amount',
        'status',
        'promo_code',
        'ordered_at'
    )
    list_filter = ('status', 'ordered_at')
    search_fields = ('user__username',)
    filter_horizontal = ('courses',)
