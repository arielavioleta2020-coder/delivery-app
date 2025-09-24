from django.urls import path
from . import views

app_name = 'restaurant'  # ¡Esto define el namespace!

urlpatterns = [
    path('', views.restaurant_list, name='restaurant_list'),
    path('menu/<int:restaurante_id>/', views.menu_restaurante, name='ver_menu'),
]