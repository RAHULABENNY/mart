from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Fresh Vegetables"
    image = models.ImageField(upload_to='categories/')
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)  # e.g., "Onion (Savala)"
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    
    # Specific fields for Instamart style
    weight = models.CharField(max_length=50)  # e.g., "1 kg", "1 Piece", "120 g"
    mrp = models.DecimalField(max_digits=7, decimal_places=2)  # The strikethrough price (e.g., 35)
    selling_price = models.DecimalField(max_digits=7, decimal_places=2)  # The actual price (e.g., 28)
    
    # Flags to organize the homepage
    is_hot_deal = models.BooleanField(default=False)  # To show in "Hot Deals" section

    def discount_percentage(self):
        # Automatically calculate the "20% OFF" badge
        if self.mrp > self.selling_price:
            discount = ((self.mrp - self.selling_price) / self.mrp) * 100
            return int(discount)
        return 0

    def __str__(self):
        return self.name
        
    @property
    def savings(self):
        if self.mrp and self.selling_price:
            return self.mrp - self.selling_price
        return 0



from django.db import models
from django.contrib.auth.models import User

# ... existing models ...

class Address(models.Model):
    ADDRESS_TYPES = (('Home', 'Home'), ('Work', 'Work'), ('Other', 'Other'))
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address_line = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    type = models.CharField(max_length=10, choices=ADDRESS_TYPES, default='Home')
    is_active = models.BooleanField(default=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.type} - {self.full_name}"
    
class Banner(models.Model):
    POSITIONS = (('Main', 'Main Big Banner'), ('Side', 'Side Small Banner'))
    
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='banners/')
    badge_text = models.CharField(max_length=50, blank=True, help_text="e.g., 'Free Delivery'")
    link = models.CharField(max_length=200, default="#", help_text="Button Link")
    position = models.CharField(max_length=10, choices=POSITIONS)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.position} - {self.title}"
    

class DeliverySetting(models.Model):
    store_latitude = models.FloatField(default=9.9312)
    store_longitude = models.FloatField(default=76.2673)
    max_delivery_radius_km = models.FloatField(default=10.0)

    def __str__(self):
        return f"Delivery Radius: {self.max_delivery_radius_km}km"