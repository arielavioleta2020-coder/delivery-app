from django.urls import path
from . import views

urlpatterns = [
    path('<int:restaurant_id>/', views.restaurant_menu, name='restaurant_menu'),
]