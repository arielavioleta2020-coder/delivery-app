from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from restaurant.models import MenuItem
from .models import Cart, CartItem

@login_required
def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user, is_active=True)
        cart_items = cart.items.all()
        total = sum(item.menu_item.price * item.quantity for item in cart_items)
    except Cart.DoesNotExist:
        cart_items = []
        total = 0
    
    # Actualizar contador en sesión
    request.session['cart_items_count'] = len(cart_items)
    
    return render(request, 'orders/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def add_to_cart(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id)
    
    # Obtener o crear el carrito del usuario
    cart, created = Cart.objects.get_or_create(
        user=request.user, 
        is_active=True
    )
    
    # Verificar si el item ya está en el carrito
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        menu_item=menu_item,
        defaults={'quantity': 1, 'price': menu_item.price}
    )
    
    if not item_created:
        # Si ya existe, aumentar la cantidad
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'¡{menu_item.name} actualizado en el carrito!')
    else:
        messages.success(request, f'¡{menu_item.name} añadido al carrito!')
    
    # Actualizar contador en sesión
    cart_items_count = cart.items.count()
    request.session['cart_items_count'] = cart_items_count
    
    # Redirigir de vuelta al menú del restaurante
    return redirect('restaurant:ver_menu', restaurante_id=menu_item.restaurant.id)

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    menu_item_name = cart_item.menu_item.name
    cart_item.delete()
    
    # Actualizar contador en sesión
    try:
        cart = Cart.objects.get(user=request.user, is_active=True)
        cart_items_count = cart.items.count()
    except Cart.DoesNotExist:
        cart_items_count = 0
    
    request.session['cart_items_count'] = cart_items_count
    messages.success(request, f'¡{menu_item_name} removido del carrito!')
    
    return redirect('orders:view_cart')

@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user, is_active=True)
        cart_items = cart.items.all()
        
        if not cart_items:
            messages.warning(request, 'Tu carrito está vacío')
            return redirect('orders:view_cart')
        
        total = sum(item.menu_item.price * item.quantity for item in cart_items)
        
        if request.method == 'POST':
            # Procesar el pedido
            # Aquí iría la lógica de procesamiento de pago, etc.
            
            # Marcar carrito como inactivo (pedido completado)
            cart.is_active = False
            cart.save()
            
            # Crear nuevo carrito vacío para el usuario
            Cart.objects.create(user=request.user, is_active=True)
            
            messages.success(request, '¡Pedido realizado con éxito!')
            request.session['cart_items_count'] = 0
            return redirect('home')
        
        return render(request, 'orders/checkout.html', {
            'cart_items': cart_items,
            'total': total
        })
        
    except Cart.DoesNotExist:
        messages.warning(request, 'No tienes un carrito activo')
        return redirect('home')

# Vista adicional para limpiar el carrito (opcional)
@login_required
def clear_cart(request):
    try:
        cart = Cart.objects.get(user=request.user, is_active=True)
        cart.items.all().delete()
        messages.success(request, 'Carrito vaciado correctamente')
        request.session['cart_items_count'] = 0
    except Cart.DoesNotExist:
        pass
    
    return redirect('orders:view_cart')

# Create your views here.



