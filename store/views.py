from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import Product, Category
from .forms import ProductForm
import json
import random
def home(request):
    hot_deals = Product.objects.filter(is_hot_deal=True) # Adjust based on your field
    
    # Get all categories that actually have products in them
    categories_with_products = Category.objects.prefetch_related('product_set').all()
    
    context = {
        'hot_deals': hot_deals,
        'categories_with_products': categories_with_products,
    }
    return render(request, 'home.html', context)


def add_product(request):
    if request.method == 'POST':
        # request.FILES is CRITICAL for uploading images
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('home')  # Redirect to the homepage to see the new item
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})


def send_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        phone = data.get('phone')
        name = data.get('name')  # 1. Get the Name
        
        otp = str(random.randint(1000, 9999))
        
        # 2. Save Name & Phone in Session
        request.session['otp'] = otp
        request.session['phone'] = phone
        request.session['temp_name'] = name 
        
        print(f"\n=== OTP FOR {name} ({phone}): {otp} ===\n")
        
        return JsonResponse({'status': 'success'})

def verify_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_otp = data.get('otp')
        
        session_otp = request.session.get('otp')
        phone = request.session.get('phone')
        name = request.session.get('temp_name') # 3. Retrieve Name
        
        if session_otp and user_otp == session_otp:
            # Create or Get User
            user, created = User.objects.get_or_create(username=phone)
            
            # 4. Update the user's name
            if name:
                user.first_name = name
                user.save()
            
            login(request, user)
            
            # Clear session data
            del request.session['otp']
            del request.session['temp_name']
            
            return JsonResponse({'status': 'success'})
        
        return JsonResponse({'status': 'error'})