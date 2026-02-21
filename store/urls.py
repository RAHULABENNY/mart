from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Pages
    path('', views.home, name='home'),
    path('add-product/', views.add_product, name='add_product'),

    # NEW: Authentication Endpoints (These fix the 404 error)
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    
    # Logout (Redirects to home)
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('cart/', views.cart_page, name='cart_page'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('dashboard/add-address/', views.add_address, name='add_address'),
    path('dashboard/edit-address/<int:id>/', views.edit_address, name='edit_address'),
    path('dashboard/delete-address/<int:id>/', views.delete_address, name='delete_address'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
]