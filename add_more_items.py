"""
Add more categories and products with real images downloaded from Unsplash.
Run: d:\mart\venv\Scripts\python add_more_items.py
"""
import os
import sys
import urllib.request
import ssl

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
import django
django.setup()

from store.models import Category, Product

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, 'media')

# Disable SSL verification for downloading (some corporate networks block it)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def download_image(url, dest_path):
    """Download an image from URL to dest_path. Returns True on success."""
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 2000:
        print(f"    [SKIP] {os.path.basename(dest_path)} already exists")
        return True
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
            data = resp.read()
            if len(data) < 1000:
                print(f"    [WARN] {os.path.basename(dest_path)} too small, skipping")
                return False
            with open(dest_path, 'wb') as f:
                f.write(data)
        print(f"    [OK] {os.path.basename(dest_path)}")
        return True
    except Exception as e:
        print(f"    [FAIL] {os.path.basename(dest_path)}: {e}")
        return False


# ============================================================
# Define NEW categories and products to add
# ============================================================

NEW_DATA = {
    # ---------- NEW CATEGORIES ----------
    'Beverages': {
        'cat_image_url': 'https://images.unsplash.com/photo-1544145945-f90425340c7e?w=400&h=300&fit=crop&q=80',
        'cat_image_file': 'categories/beverages.png',
        'products': [
            {
                'name': 'Orange Juice',
                'weight': '1 L',
                'mrp': 120,
                'selling_price': 99,
                'is_hot_deal': True,
                'image_url': 'https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?w=300&h=300&fit=crop&q=80',
                'image_file': 'products/orange_juice.png',
            },
            {
                'name': 'Green Tea',
                'weight': '25 bags',
                'mrp': 180,
                'selling_price': 149,
                'is_hot_deal': False,
                'image_url': 'https://images.unsplash.com/photo-1556881286-fc6915169721?w=300&h=300&fit=crop&q=80',
                'image_file': 'products/green_tea.png',
            },
            {
                'name': 'Mango Juice',
                'weight': '1 L',
                'mrp': 99,
                'selling_price': 85,
                'is_hot_deal': True,
                'image_url': 'https://images.unsplash.com/photo-1546173159-315724a31696?w=300&h=300&fit=crop&q=80',
                'image_file': 'products/mango_juice.png',
            },
            {
                'name': 'Coffee Powder',
                'weight': '200 g',
                'mrp': 250,
                'selling_price': 210,
                'is_hot_deal': False,
                'image_url': 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=300&h=300&fit=crop&q=80',
                'image_file': 'products/coffee.png',
            },
        ]
    },
    'Bakery': {
        'cat_image_url': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&h=300&fit=crop&q=80',
        'cat_image_file': 'categories/bakery.png',
        'products': [
            {
                'name': 'Whole Wheat Bread',
                'weight': '400 g',
                'mrp': 55,
                'selling_price': 45,
                'is_hot_deal': False,
                'image_url': 'https://images.unsplash.com/photo-1549931319-a545753467c8?w=300&h=300&fit=crop&q=80',
                'image_file': 'products/bread.png',
            },
            {
                'name': 'Butter Croissant',
                'weight': '2 Piece',
                'mrp': 90,
                'selling_price': 75,
                'is_hot_deal': True,
                'image_url': 'https://images.unsplash.com/photo-1555507036-ab1f4038024a?w=300&h=300&fit=crop&q=80',
                'image_file': 'products/croissant.png',
            },
            {
                'name': 'Chocolate Muffin',
                'weight': '1 Piece',
                'mrp': 60,
                'selling_price': 49,
                'is_hot_deal': False,
                'image_url': 'https://images.unsplash.com/photo-1607958996333-41aef7caefaa?w=300&h=300&fit=crop&q=80',
                'image_file': 'products/muffin.png',
            },
            {
                'name': 'Cookies Pack',
                'weight': '200 g',
                'mrp': 80,
                'selling_price': 65,
                'is_hot_deal': False,
                'image_url': 'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=300&h=300&fit=crop&q=80',
                'image_file': 'products/cookies.png',
            },
        ]
    },
    'Spices & Masala': {
        'cat_image_url': 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&h=300&fit=crop&q=80',
        'cat_image_file': 'categories/spices.png',
        'products': [
            {
                'name': 'Turmeric Powder',
                'weight': '100 g',
                'mrp': 45,
                'selling_price': 38,
                'is_hot_deal': False,
                'image_url': 'https://images.unsplash.com/photo-1615485500704-8e990f9900f7?w=300&h=300&fit=crop&q=80',
                'image_file': 'products/turmeric.png',
            },
            {
                'name': 'Red Chilli Powder',
                'weight': '100 g',
                'mrp': 50,
                'selling_price': 42,
                'is_hot_deal': False,
                'image_url': 'https://images.unsplash.com/photo-1599639668273-4b35013dc152?w=300&h=300&fit=crop&q=80',
                'image_file': 'products/chilli.png',
            },
            {
                'name': 'Garam Masala',
                'weight': '50 g',
                'mrp': 65,
                'selling_price': 55,
                'is_hot_deal': True,
                'image_url': 'https://images.unsplash.com/photo-1532336414038-cf19250c5757?w=300&h=300&fit=crop&q=80',
                'image_file': 'products/garam_masala.png',
            },
        ]
    },

    # ---------- MORE PRODUCTS FOR EXISTING CATEGORIES ----------
    'Fruits': {
        'cat_image_url': None,  # already exists
        'cat_image_file': None,
        'products': [
            {
                'name': 'Mango (Alphonso)',
                'weight': '1 kg',
                'mrp': 350,
                'selling_price': 299,
                'is_hot_deal': True,
                'image_url': 'https://images.unsplash.com/photo-1553279768-865429fa0078?w=300&h=300&fit=crop&q=80',
                'image_file': 'products/mango.png',
            },
            {
                'name': 'Orange',
                'weight': '1 kg',
                'mrp': 80,
                'selling_price': 65,
                'is_hot_deal': False,
                'image_url': 'https://images.unsplash.com/photo-1547514701-42782101795e?w=300&h=300&fit=crop&q=80',
                'image_file': 'products/orange.png',
            },
            {
                'name': 'Grapes (Green)',
                'weight': '500 g',
                'mrp': 70,
                'selling_price': 59,
                'is_hot_deal': False,
                'image_url': 'https://images.unsplash.com/photo-1537640538966-79f369143f8f?w=300&h=300&fit=crop&q=80',
                'image_file': 'products/grapes.png',
            },
            {
                'name': 'Pomegranate',
                'weight': '1 kg',
                'mrp': 160,
                'selling_price': 139,
                'is_hot_deal': True,
                'image_url': 'https://images.unsplash.com/photo-1615484477778-ca3b77940c25?w=300&h=300&fit=crop&q=80',
                'image_file': 'products/pomegranate.png',
            },
        ]
    },
    'Vegetables': {
        'cat_image_url': None,
        'cat_image_file': None,
        'products': [
            {
                'name': 'Tomato',
                'weight': '1 kg',
                'mrp': 40,
                'selling_price': 32,
                'is_hot_deal': False,
                'image_url': 'https://images.unsplash.com/photo-1546470427-0d4db154ceb8?w=300&h=300&fit=crop&q=80',
                'image_file': 'products/tomato.png',
            },
            {
                'name': 'Onion',
                'weight': '1 kg',
                'mrp': 45,
                'selling_price': 35,
                'is_hot_deal': False,
                'image_url': 'https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?w=300&h=300&fit=crop&q=80',
                'image_file': 'products/onion.png',
            },
            {
                'name': 'Potato',
                'weight': '1 kg',
                'mrp': 35,
                'selling_price': 28,
                'is_hot_deal': False,
                'image_url': 'https://images.unsplash.com/photo-1518977676601-b53f82aba5ee?w=300&h=300&fit=crop&q=80',
                'image_file': 'products/potato_new.png',
            },
            {
                'name': 'Capsicum (Green)',
                'weight': '250 g',
                'mrp': 30,
                'selling_price': 25,
                'is_hot_deal': False,
                'image_url': 'https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?w=300&h=300&fit=crop&q=80',
                'image_file': 'products/capsicum.png',
            },
            {
                'name': 'Broccoli',
                'weight': '1 Piece',
                'mrp': 55,
                'selling_price': 45,
                'is_hot_deal': True,
                'image_url': 'https://images.unsplash.com/photo-1459411552884-841db9b3cc2a?w=300&h=300&fit=crop&q=80',
                'image_file': 'products/broccoli.png',
            },
        ]
    },
    'Dairy': {
        'cat_image_url': None,
        'cat_image_file': None,
        'products': [
            {
                'name': 'Butter (Amul)',
                'weight': '100 g',
                'mrp': 56,
                'selling_price': 52,
                'is_hot_deal': False,
                'image_url': 'https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=300&h=300&fit=crop&q=80',
                'image_file': 'products/butter.png',
            },
            {
                'name': 'Curd (Yogurt)',
                'weight': '400 g',
                'mrp': 40,
                'selling_price': 35,
                'is_hot_deal': False,
                'image_url': 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=300&h=300&fit=crop&q=80',
                'image_file': 'products/yogurt.jpg',
            },
            {
                'name': 'Paneer',
                'weight': '200 g',
                'mrp': 90,
                'selling_price': 80,
                'is_hot_deal': True,
                'image_url': 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=300&h=300&fit=crop&q=80',
                'image_file': 'products/paneer.jpg',
            },
        ]
    },
    'Snacks': {
        'cat_image_url': None,
        'cat_image_file': None,
        'products': [
            {
                'name': 'Peanuts (Roasted)',
                'weight': '200 g',
                'mrp': 60,
                'selling_price': 49,
                'is_hot_deal': False,
                'image_url': 'https://images.unsplash.com/photo-1567095761054-7a02e69e5b2b?w=300&h=300&fit=crop&q=80',
                'image_file': 'products/peanuts.jpg',
            },
            {
                'name': 'Biscuits (Marie Gold)',
                'weight': '250 g',
                'mrp': 35,
                'selling_price': 30,
                'is_hot_deal': False,
                'image_url': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=300&h=300&fit=crop&q=80',
                'image_file': 'products/biscuits.jpg',
            },
        ]
    },
}


def main():
    print("=" * 50)
    print("  Adding Categories & Products with Images")
    print("=" * 50)

    for cat_name, cat_data in NEW_DATA.items():
        print(f"\n--- {cat_name} ---")

        # Get or create category
        category, cat_created = Category.objects.get_or_create(name=cat_name)

        # Download & assign category image if it's a new category
        if cat_data['cat_image_url'] and cat_data['cat_image_file']:
            dest = os.path.join(MEDIA_DIR, cat_data['cat_image_file'])
            if download_image(cat_data['cat_image_url'], dest):
                category.image = cat_data['cat_image_file']
                category.save()

        status = "CREATED" if cat_created else "EXISTS"
        print(f"  Category [{status}]: {cat_name}")

        # Add products
        for prod in cat_data['products']:
            # Check if product already exists
            existing = Product.objects.filter(name=prod['name'], category=category).first()
            if existing:
                print(f"  Product [EXISTS]: {prod['name']}")
                continue

            # Download product image
            img_path = os.path.join(MEDIA_DIR, prod['image_file'])
            download_image(prod['image_url'], img_path)

            # Create product
            product = Product.objects.create(
                name=prod['name'],
                category=category,
                weight=prod['weight'],
                mrp=prod['mrp'],
                selling_price=prod['selling_price'],
                is_hot_deal=prod.get('is_hot_deal', False),
                image=prod['image_file'],
            )
            print(f"  Product [CREATED]: {prod['name']} (₹{prod['selling_price']})")

    # Print summary
    print("\n" + "=" * 50)
    print(f"  Total categories: {Category.objects.count()}")
    print(f"  Total products:   {Product.objects.count()}")
    print("=" * 50)


if __name__ == '__main__':
    main()
