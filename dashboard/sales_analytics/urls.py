from django.urls import path
from . import views

app_name = 'sales_analytics'

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('dash_board/', views.dash_board, name='dash_board'),
    path('category_chart/', views.category_filter, name='category_chart'),
    path('components/', views.components, name='components'),

]
