import os
import django
import random
from django.core.files import File

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from store.models import Category, Product

def populate():
    print("Populating database...")

    categories = {
        'Fruits': {
            'image': 'categories/fruit.png',
            'products': [
                {'name': 'Apple', 'weight': '1 kg', 'mrp': 120, 'selling_price': 100, 'image': 'products/apple.png'},
                {'name': 'Banana', 'weight': '1 kg', 'mrp': 60, 'selling_price': 50, 'image': 'products/banana.png'},
            ]
        },
        'Vegetables': {
            'image': 'categories/veg.png',
            'products': [
                {'name': 'Carrot', 'weight': '500 g', 'mrp': 40, 'selling_price': 35, 'image': 'products/carrot.png'},
                {'name': 'Potato', 'weight': '1 kg', 'mrp': 50, 'selling_price': 45, 'image': 'products/potato.png'},
            ]
        },
        'Dairy': {
            'image': 'categories/dairy.png',
            'products': [
                {'name': 'Milk', 'weight': '1 L', 'mrp': 60, 'selling_price': 55, 'image': 'products/milk.png'},
                {'name': 'Cheese', 'weight': '200 g', 'mrp': 150, 'selling_price': 140, 'image': 'products/cheese.png'},
                 {'name': 'Eggs', 'weight': '6 pack', 'mrp': 70, 'selling_price': 65, 'image': 'products/eggs.png'},
            ]
        },
        'Snacks': {
            'image': 'categories/snacks.png',
            'products': [
                {'name': 'Potato Chips', 'weight': '100 g', 'mrp': 30, 'selling_price': 25, 'image': 'products/chips.png'},
                {'name': 'Chocolate Bar', 'weight': '50 g', 'mrp': 50, 'selling_price': 45, 'image': 'products/chocolate.png'},
            ]
        }
    }

    base_media_path = os.path.join(os.path.dirname(__file__), 'media')

    for cat_name, cat_data in categories.items():
        # Create or verify category
        category, created = Category.objects.get_or_create(name=cat_name)
        
        # Try to assign image if it exists in media root (simulated)
        # In a real scenario with generated images, we might need to handle this differently.
        # For now, we assume the images might be there or we skip.
        # Since I can't easily upload from script without source files, I will just set the path string
        # if the model allows it, or leave it blank if file doesn't exist.
        
        # Django ImageField stores the path relative to MEDIA_ROOT.
        # If the file exists in MEDIA_ROOT/categories/fruit.png, we can just assign the string.
        
        category.image = cat_data['image']
        category.save()
        
        print(f"{'Created' if created else 'Updated'} Category: {cat_name}")

        for prod_data in cat_data['products']:
            product, p_created = Product.objects.get_or_create(
                name=prod_data['name'],
                category=category,
                defaults={
                    'weight': prod_data['weight'],
                    'mrp': prod_data['mrp'],
                    'selling_price': prod_data['selling_price'],
                    'is_hot_deal': random.choice([True, False]),
                    'image': prod_data['image']
                }
            )
            
            if not p_created:
                # Update existing
                product.weight = prod_data['weight']
                product.mrp = prod_data['mrp']
                product.selling_price = prod_data['selling_price']
                product.image = prod_data['image']
                product.save()

            print(f"  - {'Created' if p_created else 'Updated'} Product: {prod_data['name']}")

    print("Population complete.")

if __name__ == '__main__':
    populate()
