from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from store.models import Address,Product
from .models import Order,OrderItem

# ... existing imports ...

@login_required(login_url='home')
def checkout(request):
    addresses = Address.objects.filter(user=request.user, is_active=True)
    return render(request, 'orders/checkout.html', {'addresses': addresses})


@login_required
def order_success(request):
    return render(request, 'orders/order_success.html')


@login_required(login_url='home')
def my_orders(request):
    # Fetch orders belonging to the logged-in user, newest first
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})

@login_required(login_url='home')
def user_order_detail(request, id):
    # Ensure the order belongs to the logged-in user for security
    order = get_object_or_404(Order, id=id, user=request.user)
    items = OrderItem.objects.filter(order=order)
    
    context = {
        'order': order,
        'items': items
    }
    return render(request, 'orders/user_order_detail.html', context)



import math
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from store.models import Address, DeliverySetting
from orders.models import Order,OrderItem
from store.views import is_within_range



@login_required
def place_order(request):
    if request.method == 'POST':
        try:
            # 1. Parse the incoming JSON data from the JavaScript fetch request
            data = json.loads(request.body)
            address_id = data.get('address_id')
            cart_items = data.get('cart', [])
            total_amount = data.get('total', 0)

            # 2. Validate the selected address
            try:
                address = Address.objects.get(id=address_id, user=request.user)
            except Address.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': "Invalid address selected."}, status=400)

            # 3. Check for GPS coordinates (Latitude/Longitude)
            lat = getattr(address, 'latitude', None)
            lng = getattr(address, 'longitude', None)

            if not lat or not lng:
                return JsonResponse({
                    'status': 'error', 
                    'message': "This address needs a map pin. Please add a new address or edit this one."
                }, status=400)

            # 4. Verify the address is within the store's delivery range
            allowed, distance = is_within_range(lat, lng)
            if not allowed:
                return JsonResponse({
                    'status': 'error', 
                    'message': f"Order Failed: This address is {distance}km away and outside our delivery zone."
                }, status=400)

            # 5. Save the Order to the database
            # This creates the main record for the order
            new_order = Order.objects.create(
                user=request.user,
                address=address,
                total_amount=total_amount
            )

            # 6. Save each item from the cart as an OrderItem linked to the Order
            for item in cart_items:
                # Retrieve the product ID (ensure your JS cart stores 'id' or 'product_id')
                product_id = item.get('id') or item.get('product_id')
                
                if not product_id:
                    raise ValueError(f"Cart item '{item.get('name')}' is missing a Product ID.")

                OrderItem.objects.create(
                    order=new_order,
                    product_id=product_id, 
                    price=item['price'],
                    quantity=item['quantity']
                )

            # Return success; JavaScript will handle the redirect to order_success page
            return JsonResponse({'status': 'success', 'message': "Order placed successfully!"})

        except Exception as e:
            # Log the exact error to the terminal for debugging
            print("\n==== ORDER FAILED ====")
            print(f"Error: {str(e)}")
            print("======================\n")
            
            return JsonResponse({'status': 'error', 'message': f"System Error: {str(e)}"}, status=400)
            
    return JsonResponse({'status': 'error', 'message': "Invalid request method"}, status=400)