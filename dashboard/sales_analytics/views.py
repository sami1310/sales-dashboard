from django.shortcuts import render
from django.http import HttpResponse
from .models import SalesData, Category, Region, Month
from django.db.models import Sum
from django.db.models import Avg
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from datetime import datetime
from openpyxl import Workbook
from django.shortcuts import get_object_or_404
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

    # generating total profit by taking data from the database
    total_profit = SalesData.objects.aggregate(
        total_profit=Sum('profit'))['total_profit']

    # generating average profit by taking data from the database
    average_profit = SalesData.objects.aggregate(avg_profit=Avg('profit'))
    avg_profit = average_profit['avg_profit']

    # generating total sales by taking data from the database
    total_product_sales = SalesData.objects.aggregate(
        total_sales=Sum('sales'))['total_sales']

    # getting region that sold the highest amount of products
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
    # function to generate sales data for selected 'from' to 'to' date given by the user input
    sales_data = []
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        sales_data = SalesData.objects.filter(
            sale_date__range=(start_date, end_date)).order_by('sale_date')

    return render(request, 'sales_date.html', {'sales_data': sales_data})


@login_required(login_url='../accounts/login/')
def sales_data_excel(request):
    # function to generate sales data for selected 'from' to 'to' date given by the user input in excel sheet
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    sales_data = SalesData.objects.filter(
        sale_date__range=(start_date, end_date)).order_by('sale_date')

    # Creating a new workbook and add a worksheet
    workbook = Workbook()
    worksheet = workbook.active

    # Writing the column headers to the worksheet
    worksheet.append(['Date', 'Category', 'Region', 'Sales', 'Profit'])

    # Writing the sales data to the worksheet
    for sale in sales_data:
        worksheet.append([
            sale.sale_date,
            sale.category.category_name,
            sale.region.region_name,
            sale.sales,
            sale.profit,
        ])

    # Creating an HTTP response with the Excel file
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=sales_data.xlsx'
    workbook.save(response)

    return response
