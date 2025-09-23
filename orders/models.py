from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
from restaurant.models import MenuItem
from core.models import Restaurant


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendiente'),
        ('confirmed', 'Confirmado'),
        ('preparing', 'En preparación'),
        ('on_the_way', 'En camino'),
        ('delivered', 'Entregado'),
        ('cancelled', 'Cancelado'),
    )
    
    PAYMENT_CHOICES = (
        ('cash', 'Efectivo'),
        ('card', 'Tarjeta'),
        ('digital', 'Pago digital'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash')
    payment_status = models.BooleanField(default=False)
    delivery_address = models.TextField()
    phone = models.CharField(max_length=20)
    special_instructions = models.TextField(blank=True, null=True)
    estimated_delivery_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['restaurant', 'status']),
        ]
    
    def __str__(self):
        return f"Orden #{self.id} - {self.user.username} - {self.get_status_display()}"
    
    def save(self, *args, **kwargs):
        # Calcular el total automáticamente antes de guardar
        if self.pk:
            self.total = sum(item.get_total() for item in self.items.all())
        super().save(*args, **kwargs)
    
    def can_be_cancelled(self):
        return self.status in ['pending', 'confirmed']
    
    def get_status_class(self):
        status_classes = {
            'pending': 'warning',
            'confirmed': 'info',
            'preparing': 'primary',
            'on_the_way': 'success',
            'delivered': 'secondary',
            'cancelled': 'danger',
        }
        return status_classes.get(self.status, 'secondary')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    class Meta:
        unique_together = ['order', 'menu_item']
    
    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} - ${self.get_total():.2f}"

    def get_total(self):
        return self.quantity * self.price


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Carrito de {self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    def get_total(self):
        return sum(item.get_total() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['cart', 'menu_item']
    
    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"
    
    def get_total(self):
        return self.quantity * self.menu_item.price