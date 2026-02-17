from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from store.models import Product, Category
from store.forms import ProductForm,CategoryForm


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
            messages.success(request, 'Product added successfully!')
        else:
            messages.error(request, 'Error adding product. Please check the data.')
    return redirect('roduct_list_admin')


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