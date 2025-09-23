from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Restaurant, MenuItem  

def home(request):
    # Obtener algunos restaurantes destacados para la página de inicio
    featured_restaurants = Restaurant.objects.filter(is_featured=True)[:4]
    
    # Calcular items en el carrito si el usuario está autenticado
    cart_items_count = 0
    if request.user.is_authenticated:
        try:
            # Importación local para evitar problemas circulares
            from orders.models import Cart
            cart = Cart.objects.get(user=request.user, is_active=True)
            cart_items_count = cart.items.count()
        except:
            pass
    
    return render(request, 'home.html', {
        'featured_restaurants': featured_restaurants,
        'cart_items_count': cart_items_count
    })

def restaurant_list(request):
    restaurants = Restaurant.objects.all()  
    
    # Calcular items en el carrito
    cart_items_count = 0
    if request.user.is_authenticated:
        try:
            # Importación local para evitar problemas circulares
            from orders.models import Cart
            cart = Cart.objects.get(user=request.user, is_active=True)
            cart_items_count = cart.items.count()
        except:
            pass
    
    return render(request, 'restaurant/list.html', {
        'restaurants': restaurants,
        'cart_items_count': cart_items_count
    })

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = MenuItem.objects.filter(restaurant=restaurant, available=True)
    
    # Calcular items en el carrito
    cart_items_count = 0
    if request.user.is_authenticated:
        try:
            # Importación local para evitar problemas circulares
            from orders.models import Cart
            cart = Cart.objects.get(user=request.user, is_active=True)
            cart_items_count = cart.items.count()
        except:
            pass
    
    return render(request, 'restaurant/detail.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
        'cart_items_count': cart_items_count
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Cuenta creada para {username}!')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    # Calcular items en el carrito
    cart_items_count = 0
    if request.user.is_authenticated:
        try:
            # Importación local para evitar problemas circulares
            from orders.models import Cart
            cart = Cart.objects.get(user=request.user, is_active=True)
            cart_items_count = cart.items.count()
        except:
            pass
    
    return render(request, 'registration/register.html', {
        'form': form,
        'cart_items_count': cart_items_count
    })