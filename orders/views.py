from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from restaurant.models import MenuItem

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


# Create your views here.



