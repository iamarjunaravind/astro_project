from django.urls import path
from . import views, payment_views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    # Payment Routes
    path('wallet/recharge/', payment_views.create_recharge_order, name='create_recharge'),
    path('wallet/verify/', payment_views.verify_payment, name='verify_payment'),
]
