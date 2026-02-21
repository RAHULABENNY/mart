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
    

def cart_page(request):
    return render(request, 'cart.html')


from django.contrib.auth.decorators import login_required

# ... your other imports ...

@login_required(login_url='home')  
def user_dashboard(request):
    addresses = Address.objects.filter(user=request.user, is_active=True)
    return render(request, 'user_dashboard.html')

login_required
def user_dashboard(request):
    
    # ---------------------------------------------------------
    # THE FIX: Add is_active=True so "deleted" addresses stay hidden!
    # ---------------------------------------------------------
    addresses = Address.objects.filter(user=request.user, is_active=True).order_by('-id')
    
    # Example: Fetching orders for the dashboard (if you have them)
    # orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'addresses': addresses,
        # 'orders': orders,
    }
    return render(request, 'user_dashboard.html', context)



from .models import Address

import math
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from store.models import DeliverySetting
from store.forms import AddressForm

def is_within_range(user_lat, user_lng):
    setting = DeliverySetting.objects.get(id=1)
    R = 6371.0  # Radius of Earth in km

    # Convert to Radians
    lat1, lon1 = math.radians(setting.store_latitude), math.radians(setting.store_longitude)
    lat2, lon2 = math.radians(float(user_lat)), math.radians(float(user_lng))

    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance <= setting.max_delivery_radius_km, round(distance, 2)

@login_required
def add_address(request):
    if request.method == 'POST':
        # 1. Capture Latitude/Longitude from hidden fields in user dashboard map
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')

        if lat and lng:
            allowed, distance = is_within_range(lat, lng)
            if not allowed:
                messages.error(request, f"Out of Range! You are {distance}km away. We only deliver within range.")
                return redirect('user_dashboard')

        # 2. Standard Form Processing
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            
            # ---------------------------------------------------------
            # THE FIX: Explicitly save the coordinates to the database!
            # ---------------------------------------------------------
            if lat and lng:
                address.latitude = lat
                address.longitude = lng
                
            address.save()
            messages.success(request, "Address added successfully!")
        else:
            messages.error(request, "Error in form inputs.")
            
    return redirect('user_dashboard')


from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Address

@login_required
def delete_address(request, id):
    # Securely fetch the address ensuring it belongs to the logged-in user
    address = get_object_or_404(Address, id=id, user=request.user)
    
    # Soft Delete: Mark as inactive so it doesn't break past orders
    address.is_active = False
    address.save()
    
    messages.success(request, "Address deleted successfully.")
    
    # Redirect specifically to the dashboard's address tab
    return redirect(reverse('user_dashboard') + '#addresses')


@login_required
def edit_address(request, id):
    # Ensure the address belongs to the logged-in user
    address = get_object_or_404(Address, id=id, user=request.user)
    
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            updated_address = form.save(commit=False)
            
            # Grab the new coordinates in case the user moved the map pin
            lat = request.POST.get('lat')
            lng = request.POST.get('lng')
            
            # Ensure we update the map coordinates
            if lat and lng:
                updated_address.latitude = lat
                updated_address.longitude = lng
                
            updated_address.save()
            messages.success(request, "Address updated successfully!")
        else:
            messages.error(request, "Error updating address. Please check inputs.")
            
    return redirect('user_dashboard')

from .models import Product, Category, Banner

def home(request):
    # CHANGED: Fetch ALL active main banners, not just .first()
    main_banners = Banner.objects.filter(position='Main', is_active=True)
    
    side_banner = Banner.objects.filter(position='Side', is_active=True).first()
    hot_deals = Product.objects.filter(is_hot_deal=True)
    categories = Category.objects.all()
    
    context = {
        'main_banners': main_banners, # Changed key name
        'side_banner': side_banner,
        'hot_deals': hot_deals,
        'categories_with_products': categories,
    }
    return render(request, 'home.html', context)


from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def category_products(request, category_id):
    # Fetch the specific category
    category = get_object_or_404(Category, id=category_id)
    # Fetch all products belonging to this category
    products = Product.objects.filter(category=category)
    
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'category_products.html', context)


from django.http import JsonResponse
from .models import Product # Use your actual Product model name

def search_suggestions(request):
    query = request.GET.get('q', '')
    if len(query) > 1:
        # Search for products starting with or containing the query
        results = Product.objects.filter(name__icontains=query)[:6]
        data = [{'id': p.id, 'name': p.name} for p in results]
        return JsonResponse({'results': data})
    return JsonResponse({'results': []})



from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, id):
    # This will fetch product #9 or show a 404 if it doesn't exist in the DB
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})

