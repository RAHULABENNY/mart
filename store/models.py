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
