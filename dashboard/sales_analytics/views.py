from django.shortcuts import render
from django.http import HttpResponse
from .models import SalesData, Category, Region, Month
from django.db.models import Sum
from django.db.models import Avg
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# Create your views here.


def home_view(request):
    return render(request, 'base.html')


@login_required(login_url='../accounts/login/')
def dash_board(request):

    # queryset to generate profits per month
    # grouping by months in values[...] and aggregating total profit that was grouped by months
    # example output for this queryset --> {'month__month_name': 'March', 'total_profit': 3500.0}
    queryset = SalesData.objects.values('month__month_name').annotate(
        total_profit=Sum('profit'))

    # looping through the dictionary retrived by the 'queryset' and extracting month name
    # that month name is being added as  labels for x-axis for the graph
    # total profit for each month is being added as datas for y-axis for the graph
    labels = [data['month__month_name'] for data in queryset]
    data = [data['total_profit'] for data in queryset]

    # queryset2 to generate profits per region chart
    # Region in x-axis Profit in y-axis
    queryset2 = SalesData.objects.values(
        'region__region_name').annotate(total_profit=Sum('profit'))
    labels2 = [data['region__region_name'] for data in queryset2]
    data2 = [data['total_profit'] for data in queryset2]

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
        'labels2': labels2,
        'data2': data2,
        'total_profit': total_profit,
        'avg_profit': avg_profit,
        'total_product_sales': total_product_sales,
        'region_name': region_name,

    }

    return render(request, 'dashboard.html', context)


@login_required(login_url='../accounts/login/')
def category_filter(request):

    # output by this query --> {'category__category_name': 'Sports', 'total_sale': 12}
    queryset = SalesData.objects.values(
        'category__category_name').annotate(total_sale=Sum('sales'))

    # taking category and sales as label field as x-axis and y-axis
    labels = [data['category__category_name'] for data in queryset]
    data = [data['total_sale'] for data in queryset]

    # creating a list of dictionaries for each category and its total sales
    # output [{'category': 'Sports', 'total_sale': 12}, {'category': 'Electronics', 'total_sale': 14}..,.]
    # this is needed for generating the table beside the chart
    categories = [{'category': labels[i], 'total_sale': data[i]}
                  for i in range(len(labels))]

    context = {
        'labels': labels,
        'data': data,
        'categories': categories,
    }

    return render(request, 'category_chart.html', context)


@login_required(login_url='../accounts/login/')
def region_filter(request):

    # output by this query --> {'category__category_name': 'Sports', 'total_sale': 12}
    queryset = SalesData.objects.values(
        'region__region_name').annotate(total_sale=Sum('sales'))

    # taking category and sales as label field as x-axis and y-axis
    labels = [data['region__region_name'] for data in queryset]
    data = [data['total_sale'] for data in queryset]

    regions = [{'region': labels[i], 'total_sale': data[i]}
               for i in range(len(labels))]

    context = {
        'labels': labels,
        'data': data,
        'regions': regions,
    }

    return render(request, 'region_chart.html', context)


@login_required(login_url='../accounts/login/')
def month_filter(request):

    # output by this query --> {'category__category_name': 'Sports', 'total_sale': 12}
    queryset = SalesData.objects.values(
        'month__month_name').annotate(total_sale=Sum('sales'))

    # taking category and sales as label field as x-axis and y-axis
    labels = [data['month__month_name'] for data in queryset]
    data = [data['total_sale'] for data in queryset]

    months = [{'month': labels[i], 'total_sale': data[i]}
              for i in range(len(labels))]
    context = {
        'labels': labels,
        'data': data,
        'months': months,
    }

    return render(request, 'month_chart.html', context)


@login_required(login_url='../accounts/login/')
def sales_data_by_date(request):
    sales_data = []
    if request.method == 'POST':
        date = request.POST.get('date')
        sales_data = SalesData.objects.filter(sale_date=date)
    return render(request, 'sales_date.html', {'sales_data': sales_data})
