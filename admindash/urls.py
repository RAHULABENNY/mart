from django.urls import path
from . import views

urlpatterns = [
    path('admin_dash', views.admin_dashboard, name='admin_dashboard'),  
    path('admin_products/', views.product_list_admin, name='product_list_admin'),
    path('category-list/', views.category_list, name='category_list'),
    path('adminlogin/', views.admin_login, name='admin_login'),    
    path('add-product/', views.add_product, name='add_product'),
    path('add-category/', views.add_category, name='add_category'),
    path('dash/product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('dash/product/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('dash/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('dash/category/delete/<int:pk>/', views.delete_category, name='delete_category'),
    path('orders/', views.admin_order_list, name='admin_order_list'),
    path('orders/<int:id>/', views.admin_order_detail, name='admin_order_detail'),
    path('products/bulk-delete/', views.bulk_delete_products, name='bulk_delete_products'),
    path('banners/', views.banner_list, name='banner_list'),
    path('banners/add/', views.add_banner, name='add_banner'),
    path('banners/edit/<int:id>/', views.edit_banner, name='edit_banner'),
    path('banners/delete/<int:id>/', views.delete_banner, name='delete_banner'),
    path('settings/location/', views.location_settings, name='location_settings'),
]