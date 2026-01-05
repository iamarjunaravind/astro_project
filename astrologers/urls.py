from django.urls import path
from . import views

app_name = 'astrologers'

urlpatterns = [
    path('', views.astrologer_list, name='astrologer_list'),
    path('<int:pk>/', views.astrologer_detail, name='astrologer_detail'),
]
