from django.urls import path
from . import views

app_name = 'kundali'

urlpatterns = [
    path('', views.kundali_input, name='kundali_form'),
]
