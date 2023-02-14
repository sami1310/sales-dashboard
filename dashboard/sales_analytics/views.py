from django.shortcuts import render
from django.http import HttpResponse
from .models import SalesData, Category, Region, Month

# Create your views here.


def home_page(request):
    return render(request, 'base.html')


def dash_board(request):
    sales_data = SalesData.objects.all()
    labels = []
    data = []
    for entry in sales_data:
        label = entry.category.category_name + ' - ' + \
            entry.region.region_name + ' - ' + entry.month.month_name
        labels.append(label)
        data.append(entry.sales)
        context = {
            'labels': labels,
            'data': data,
        }

    return render(request, 'dashboard.html', context)
