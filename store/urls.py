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
]