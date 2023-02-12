from django.shortcuts import render
from django.http import HttpResponse
from .models import SalesData, Category, Region, Month

# Create your views here.


def home_page(request):

    return render(request, 'dashboard.html')
