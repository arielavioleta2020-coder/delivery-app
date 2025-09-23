from django.contrib import admin
from .models import OrderItem

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'quantity', 'price')
    
    def product_name(self, obj):
        return obj.product.name  # Suponiendo que el modelo Product tiene un campo 'name'
    product_name.short_description = 'Product'  # Personaliza el nombre de la columna

admin.site.register(OrderItem, OrderItemAdmin)
