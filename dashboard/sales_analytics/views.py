from django.shortcuts import render
from django.http import HttpResponse
from .models import SalesData, Category, Region, Month
from django.db.models import Sum

# Create your views here.


def home_page(request):
    return render(request, 'base.html')


def dash_board(request):

    # grouping by months in values[...] and aggregating total profit that was grouped by months
    # example output of this queryset --> {'month__month_name': 'March', 'total_profit': 3500.0}
    queryset = SalesData.objects.values('month__month_name').annotate(
        total_profit=Sum('profit'))

    # looping through the dictionary retrived by the 'queryset' and extracting month name
    # that month name is being added as  labels for x-axis for the graph
    labels = [data['month__month_name'] for data in queryset]

    # total profit for each month is being added as datas for y-axis for the graph
    data = [data['total_profit'] for data in queryset]

    # data and labels are being passed as context in the dashboard.html file
    context = {
        'labels': labels,
        'data': data,
    }

    return render(request, 'dashboard.html', context)
