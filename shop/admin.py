from django.contrib import admin
from .models import Category, Product

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'parent']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['parent']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'author', 'category',
        'price', 'old_price', 'stock',
        'available', 'is_featured'
    ]
    list_filter = ['available', 'is_featured', 'category', 'created']
    list_editable = ['price', 'stock', 'available', 'is_featured']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'author', 'description']
    list_per_page = 20
    fieldsets = (
        ('Основна інформація', {
            'fields': ('category', 'name', 'slug', 'author', 'publisher')
        }),
        ('Опис та медіа', {
            'fields': ('description', 'cover')
        }),
        ('Ціна та склад', {
            'fields': ('price', 'old_price', 'stock', 'available')
        }),
        ('Додатково', {
            'fields': ('is_featured', 'rating', 'rating_count')
        }),
    )