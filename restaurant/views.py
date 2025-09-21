from django.shortcuts import render, get_object_or_404
from core.models import Restaurant
from .models import MenuItem

def restaurant_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = MenuItem.objects.filter(restaurant=restaurant, available=True)
    return render(request, 'restaurant/menu.html', {
        'restaurant': restaurant,
        'menu_items': menu_items
    })

# Create your views here.
