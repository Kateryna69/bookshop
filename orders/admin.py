from django.contrib import admin
from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['get_cost']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'first_name', 'last_name',
        'email', 'status', 'total_price', 'created'
    ]
    list_filter = ['status', 'created']
    list_editable = ['status']
    search_fields = ['first_name', 'last_name', 'email']
    inlines = [OrderItemInline]
    readonly_fields = ['total_price', 'created', 'updated']