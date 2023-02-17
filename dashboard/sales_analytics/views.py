from django.shortcuts import render
from django.http import HttpResponse
from .models import SalesData, Category, Region, Month
from django.db.models import Sum
from django.db.models import Avg
# Create your views here.


def dash_board(request):

    # grouping by months in values[...] and aggregating total profit that was grouped by months
    # example output for this queryset --> {'month__month_name': 'March', 'total_profit': 3500.0}
    queryset = SalesData.objects.values('month__month_name').annotate(
        total_profit=Sum('profit'))

    # looping through the dictionary retrived by the 'queryset' and extracting month name
    # that month name is being added as  labels for x-axis for the graph
    # total profit for each month is being added as datas for y-axis for the graph
    labels = [data['month__month_name'] for data in queryset]
    data = [data['total_profit'] for data in queryset]

    total_profit = SalesData.objects.aggregate(
        total_profit=Sum('profit'))['total_profit']
    average_profit = SalesData.objects.aggregate(avg_profit=Avg('profit'))
    avg_profit = average_profit['avg_profit']

    total_product_sales = SalesData.objects.aggregate(
        total_sales=Sum('sales'))['total_sales']

    highest_sale = SalesData.objects.values('region__region_name').annotate(
        total_sales=Sum('sales')).order_by('-total_sales').first()
    region_name = highest_sale['region__region_name']

    # data and labels are being passed as context in the dashboard.html file
    context = {
        'labels': labels,
        'data': data,
        'total_profit': total_profit,
        'avg_profit': avg_profit,
        'total_product_sales': total_product_sales,
        'region_name': region_name,

    }

    return render(request, 'dashboard.html', context)


def category_filter(request):

    # output by this query --> {'category__category_name': 'Sports', 'total_sale': 12}
    queryset = SalesData.objects.values(
        'category__category_name').annotate(total_sale=Sum('sales'))

    # taking category and sales as label field as x-axis and y-axis
    labels = [data['category__category_name'] for data in queryset]
    data = [data['total_sale'] for data in queryset]
    context = {
        'labels': labels,
        'data': data,
    }

    return render(request, 'category_chart.html', context)


def components(request):
    total_profit = SalesData.objects.aggregate(
        total_profit=Sum('profit'))['total_profit']
    average_profit = SalesData.objects.aggregate(avg_profit=Avg('profit'))

    context = {
        'total_profit': total_profit,
        'average_profit': average_profit,
    }

    return render(request, 'dashboard.html', context)
