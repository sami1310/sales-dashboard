from django.urls import path
from . import views

app_name = 'sales_analytics'

urlpatterns = [
    path('', views.dash_board, name='dash_board'),
    path('home/', views.home_page, name='home'),
]
