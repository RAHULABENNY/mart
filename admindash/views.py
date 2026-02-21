from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from store.models import Product, Category
from store.forms import ProductForm,CategoryForm
from django.urls import reverse


@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    product_count = Product.objects.count()
    category_count = Category.objects.count()

    context = {
        'product_count': product_count,
        'category_count': category_count,
    }
    return render(request, 'admindash/dashboard.html', context)



@user_passes_test(lambda u: u.is_staff)
def category_list(request):
    categories = Category.objects.all().order_by('-id')
    return render(request, 'admindash/category_list.html', {
        'categories': categories
    })


def product_list_admin(request):
    products = Product.objects.all().order_by('-id')
    categories = Category.objects.all()
    form = ProductForm()  # Empty form for the modal
    
    context = {
        'products': products,
        'categories': categories,
        'form': form
    }
    return render(request, 'admindash/product_list.html', context)


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            
            # Check which button was clicked
            action = request.POST.get('action')
            
            if action == 'save_add_another':
                # Redirect back to list but with a parameter to open modal again
                return redirect(f"{reverse('product_list_admin')}?add_another=True")
            
            # Default: just go back to list
            return redirect('product_list')

# THIS WAS LIKELY MISSING OR MISSPELLED
@user_passes_test(lambda u: u.is_staff)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('category_list')   # go back to list page
    else:
        form = CategoryForm()

    categories = Category.objects.all().order_by('-id')

    return render(request, 'admindash/category_list.html', {
        'form': form,
        'categories': categories
    })



from django.shortcuts import get_object_or_404



@user_passes_test(lambda u: u.is_staff)
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        # 'instance=product' tells Django to update this specific record
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list_admin')
    
    # If the form is invalid or GET request, redirect back to list
    return redirect('product_list_admin')

@user_passes_test(lambda u: u.is_staff)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product_list_admin')
    return render(request, 'admindash/confirm_delete.html', {'item': product, 'type': 'Product'})



@user_passes_test(lambda u: u.is_staff)
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'admindash/edit_category.html', {'form': form, 'category': category})

@user_passes_test(lambda u: u.is_staff)
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    return render(request, 'admindash/confirm_delete.html', {'item': category, 'type': 'Category'})




from django.contrib.auth import authenticate, login
from django.contrib import messages

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)

        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Access Denied: Staff only.")
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'admindash/login.html')




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from orders.models import Order, OrderItem

# ... existing admin views ...

@user_passes_test(lambda u: u.is_staff)
def admin_order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'admindash/order_list.html', {'orders': orders})

@user_passes_test(lambda u: u.is_staff)
def admin_order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    order_items = OrderItem.objects.filter(order=order)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        messages.success(request, f'Order #{order.id} status updated to {new_status}')
        return redirect('admin_order_detail', id=id)

    context = {
        'order': order,
        'order_items': order_items,
        'status_choices': Order.STATUS_CHOICES
    }
    return render(request, 'admindash/order_detail.html', context)



def bulk_delete_products(request):
    if request.method == 'POST':
        # Get the list of IDs from the form
        product_ids = request.POST.getlist('product_ids')
        
        if product_ids:
            # Delete all selected products
            Product.objects.filter(id__in=product_ids).delete()
            messages.success(request, f"{len(product_ids)} products deleted successfully!")
        else:
            messages.warning(request, "No products selected.")
            
    return redirect('product_list_admin')




from store.models import Banner  # Import Banner Model

# 1. List Banners
def banner_list(request):
    banners = Banner.objects.all().order_by('-created_at')
    return render(request, 'admindash/banner_list.html', {'banners': banners})

# 2. Add Banner
def add_banner(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        subtitle = request.POST.get('subtitle')
        image = request.FILES.get('image')
        badge_text = request.POST.get('badge_text')
        link = request.POST.get('link')
        position = request.POST.get('position')
        is_active = request.POST.get('is_active') == 'on'

        Banner.objects.create(
            title=title,
            subtitle=subtitle,
            image=image,
            badge_text=badge_text,
            link=link,
            position=position,
            is_active=is_active
        )
        messages.success(request, "Banner added successfully!")
        return redirect('banner_list')

# 3. Edit Banner
def edit_banner(request, id):
    banner = get_object_or_404(Banner, id=id)
    if request.method == 'POST':
        banner.title = request.POST.get('title')
        banner.subtitle = request.POST.get('subtitle')
        
        # Only update image if a new one is uploaded
        if request.FILES.get('image'):
            banner.image = request.FILES.get('image')
            
        banner.badge_text = request.POST.get('badge_text')
        banner.link = request.POST.get('link')
        banner.position = request.POST.get('position')
        banner.is_active = request.POST.get('is_active') == 'on'
        banner.save()
        messages.success(request, "Banner updated successfully!")
        return redirect('banner_list')

# 4. Delete Banner
def delete_banner(request, id):
    banner = get_object_or_404(Banner, id=id)
    banner.delete()
    messages.success(request, "Banner deleted successfully!")
    return redirect('banner_list')



from store.models import DeliverySetting  # Import from store app

def location_settings(request):
    # Get the single settings instance
    setting, _ = DeliverySetting.objects.get_or_create(id=1)

    if request.method == "POST":
        setting.store_latitude = float(request.POST.get('lat'))
        setting.store_longitude = float(request.POST.get('lng'))
        setting.max_delivery_radius_km = float(request.POST.get('radius'))
        setting.save()
        messages.success(request, "Delivery range updated successfully!")
        return redirect('location_settings')

    context = {
        'store_lat': setting.store_latitude,
        'store_lng': setting.store_longitude,
        'current_range': setting.max_delivery_radius_km,
    }
    return render(request, 'admindash/location_settings.html', context)
