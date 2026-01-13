from django.urls import path
from . import views, payment_views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('verify-phone-auth/', views.verify_phone_auth, name='verify_phone_auth'),
    path('register/', views.register_view, name='register'),
    path('register/astrologer/', views.register_astrologer_view, name='register_astrologer'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    # Recharge Page (UI)
    path('wallet/', views.recharge_view, name='recharge_page'),
    
    # Payment API Routes
    path('api/recharge/', payment_views.create_recharge_order, name='recharge'), 
    path('api/verify-payment/', payment_views.verify_payment, name='verify_payment'),
    
    # Admin Dashboard URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Product Management
    path('admin-dashboard/products/', views.admin_product_list, name='admin_product_list'),
    path('admin-dashboard/products/add/', views.admin_product_add, name='admin_product_add'),
    path('admin-dashboard/products/edit/<int:pk>/', views.admin_product_edit, name='admin_product_edit'),
    
    # Astrologer Verification
    path('admin-dashboard/astrologers/', views.admin_astrologer_list, name='admin_astrologer_list'),
    path('admin-dashboard/astrologers/verify/<int:pk>/', views.admin_verify_astrologer, name='admin_verify_astrologer'),
    path('admin-dashboard/users/', views.admin_user_list, name='admin_user_list'),
    path('admin-dashboard/users/delete/<int:user_id>/', views.admin_delete_user, name='admin_delete_user'),
    
    # Order Management
    path('admin-dashboard/orders/', views.admin_order_list, name='admin_order_list'),
    path('admin-dashboard/orders/update-status/<int:pk>/', views.admin_update_order_status, name='admin_update_order_status'),
]
