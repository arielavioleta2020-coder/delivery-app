from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='restaurants/', blank=True)
    categories = models.ManyToManyField(Category)
    
    def __str__(self):
        return self.name


# Create your models here.
