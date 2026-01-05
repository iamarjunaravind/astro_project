from django.urls import path
from . import views

app_name = 'horoscope'

urlpatterns = [
    # List views for different periods
    path('', views.horoscope_list, {'period': 'daily', 'day': 'today'}, name='horoscope_list'),
    path('daily/<str:day>/', views.horoscope_list, {'period': 'daily'}, name='horoscope_daily'),
    path('weekly/', views.horoscope_list, {'period': 'weekly', 'day': None}, name='horoscope_weekly'),
    path('monthly/', views.horoscope_list, {'period': 'monthly', 'day': None}, name='horoscope_monthly'),
    path('yearly/', views.horoscope_list, {'period': 'yearly', 'day': None}, name='horoscope_yearly'),

    # Detail views
    path('daily/<str:day>/<str:sign>/', views.horoscope_detail, {'period': 'daily'}, name='horoscope_detail_daily'),
    path('weekly/<str:sign>/', views.horoscope_detail, {'period': 'weekly', 'day': None}, name='horoscope_detail_weekly'),
    path('monthly/<str:sign>/', views.horoscope_detail, {'period': 'monthly', 'day': None}, name='horoscope_detail_monthly'),
    path('yearly/<str:sign>/', views.horoscope_detail, {'period': 'yearly', 'day': None}, name='horoscope_detail_yearly'),
]
