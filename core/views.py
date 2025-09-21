from django.shortcuts import render
from .models import Restaurant

def home(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'core/home.html', {'restaurants': restaurants})




# Create your views here.
