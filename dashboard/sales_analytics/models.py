from django.db import models

# Create your models here.
CATEGORY_CHOICES = (
    ('D', 'Desktop'),
    ('L', 'Laptop'),
    ('M', 'Mobile'),
    ('C', 'Camera'),
    ('K', 'Keyboard')
)

class Product(models.Model):
    title = models.CharField(max_length=40)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    price = models.FloatField()

class Ordered(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    ordered_date = models.DateTimeField()
    region = models.CharField(max_length=10)