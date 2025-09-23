from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from restaurant.models import MenuItem
from .models import Cart, CartItem

@login_required
def add_to_cart(request, item_id):
    item = MenuItem.objects.get(id=item_id)
    
    cart = request.session.get('cart', {})
    
    if str(item_id) in cart:
        cart[str(item_id)]['quantity'] += 1
    else:
        cart[str(item_id)] = {
            'name': item.name,
            'price': str(item.price),
            'quantity': 1,
            'image': item.image.url if item.image else ''
        }
    
    request.session['cart'] = cart
    messages.success(request, f'{item.name} añadido al carrito')
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    total = sum(float(item['price']) * item['quantity'] for item in cart.values())
    return render(request, 'orders/cart.html', {'cart': cart, 'total': total})

@login_required
def checkout(request):
    # Lógica simplificada para el checkout
    if request.method == 'POST':
        # Procesar el pedido
        request.session['cart'] = {}
        messages.success(request, 'Pedido realizado con éxito')
        return redirect('home')
    
    cart = request.session.get('cart', {})
    total = sum(float(item['price']) * item['quantity'] for item in cart.values())
    return render(request, 'orders/checkout.html', {'cart': cart, 'total': total})

def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()
          
        cart = Cart.objects.get(user=request.user, is_active=True)
        request.session['cart_items_count'] = cart.items.count()
    return redirect('view_cart')

def some_view(request):
    # Tu lógica de vista aquí
    cart = Cart.objects.get(user=request.user, is_active=True)
    # ... resto del código
    return render(request, 'template.html', context)

# Create your views here.



