from django.contrib import admin
from .models import Category, Supplier, Product, StockMovement

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_register = ('name', 'contact', 'phone', 'email')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'category', 'supplier', 'price', 'stock', 'min_stock', 'alert_stock')
    list_filter = ('category', 'supplier') 
    search_fields = ('sku', 'name')

    @admin.display(description='Alerta Stock', boolean=True)
    def alert_stock(self, obj):
        return obj.is_low_stock

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'movement_type', 'quantity', 'date', 'notes')
    list_filter = ('movement_type', 'date', 'product__category')
    search_fields = ('product__name', 'product__sku')
