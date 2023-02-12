from django.contrib import admin
from .models import Category, Region, Month, SalesData
# Register your models here.

admin.site.register(Category)
admin.site.register(Region)
admin.site.register(Month)
admin.site.register(SalesData)