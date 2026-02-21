"""
Add hot deal products and mark existing high-discount items as hot deals.
"""
import os, urllib.request, ssl

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
import django
django.setup()

from store.models import Category, Product

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media')


def download(url, rel_path):
    full = os.path.join(BASE, rel_path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    if os.path.exists(full) and os.path.getsize(full) > 2000:
        return True
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
            data = resp.read()
            with open(full, 'wb') as f:
                f.write(data)
        print(f'    [OK] {rel_path}')
        return True
    except Exception as e:
        print(f'    [FAIL] {rel_path}: {e}')
        return False


# ============================================================
# STEP 1: Mark existing high-discount products as Hot Deals
# ============================================================
print('=' * 55)
print('  STEP 1: Marking existing products as Hot Deals')
print('=' * 55)

# Products with good discounts that should be hot deals
mark_ids = [
    20,  # kiwi - 42% off
    21,  # sunflower oil - 44% off
    22,  # B-Rice - 20% off
    38,  # Orange - 19% off
    39,  # Grapes - 16% off
    41,  # Tomato - 20% off
    42,  # Onion - 22% off
    56,  # Lemon - 25% off
    60,  # Green Chilli - 33% off
    33,  # Cookies Pack - 19% off
    49,  # Peanuts - 18% off
    29,  # Coffee Powder - 16% off
]

for pid in mark_ids:
    try:
        p = Product.objects.get(id=pid)
        if not p.is_hot_deal:
            p.is_hot_deal = True
            p.save()
            print(f'  [MARKED] {p.name} ({p.discount_percentage()}% OFF)')
        else:
            print(f'  [SKIP]   {p.name} (already hot deal)')
    except Product.DoesNotExist:
        print(f'  [SKIP]   ID {pid} not found')


# ============================================================
# STEP 2: Add NEW exclusive hot deal products with big discounts
# ============================================================
print('\n' + '=' * 55)
print('  STEP 2: Adding NEW Hot Deal Products')
print('=' * 55)

NEW_HOT_DEALS = [
    {
        'name': 'Almond (Badam)',
        'category': 'Snacks',
        'weight': '250 g',
        'mrp': 320,
        'selling_price': 199,  # 38% OFF
        'image_url': 'https://images.unsplash.com/photo-1508061253366-f7da158b6d46?w=300&h=300&fit=crop&q=80',
        'image_file': 'products/almonds.png',
    },
    {
        'name': 'Cashew Nuts (Kaju)',
        'category': 'Snacks',
        'weight': '250 g',
        'mrp': 350,
        'selling_price': 249,  # 29% OFF
        'image_url': 'https://images.unsplash.com/photo-1563292769-4cf8a8327a44?w=300&h=300&fit=crop&q=80',
        'image_file': 'products/cashew.png',
    },
    {
        'name': 'Olive Oil (Extra Virgin)',
        'category': 'oils',
        'weight': '500 ml',
        'mrp': 450,
        'selling_price': 299,  # 34% OFF
        'image_url': 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=300&h=300&fit=crop&q=80',
        'image_file': 'products/olive_oil.png',
    },
    {
        'name': 'Honey (Pure)',
        'category': 'Beverages',
        'weight': '500 g',
        'mrp': 350,
        'selling_price': 229,  # 35% OFF
        'image_url': 'https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=300&h=300&fit=crop&q=80',
        'image_file': 'products/honey.png',
    },
    {
        'name': 'Dark Chocolate (70%)',
        'category': 'Snacks',
        'weight': '100 g',
        'mrp': 180,
        'selling_price': 119,  # 34% OFF
        'image_url': 'https://images.unsplash.com/photo-1549007994-cb92caebd54b?w=300&h=300&fit=crop&q=80',
        'image_file': 'products/dark_chocolate.png',
    },
    {
        'name': 'Basmati Rice (Premium)',
        'category': 'Rice',
        'weight': '5 kg',
        'mrp': 550,
        'selling_price': 399,  # 27% OFF
        'image_url': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=300&h=300&fit=crop&q=80',
        'image_file': 'products/basmati_rice.png',
    },
    {
        'name': 'Avocado',
        'category': 'Fruits',
        'weight': '2 Piece',
        'mrp': 180,
        'selling_price': 119,  # 34% OFF
        'image_url': 'https://images.unsplash.com/photo-1523049673857-eb18f1d7b578?w=300&h=300&fit=crop&q=80',
        'image_file': 'products/avocado.png',
    },
    {
        'name': 'Mixed Dry Fruits Pack',
        'category': 'Snacks',
        'weight': '500 g',
        'mrp': 599,
        'selling_price': 399,  # 33% OFF
        'image_url': 'https://images.unsplash.com/photo-1604068549290-dea0e4a305ca?w=300&h=300&fit=crop&q=80',
        'image_file': 'products/dry_fruits.png',
    },
]

for item in NEW_HOT_DEALS:
    cat_name = item.pop('category')
    try:
        cat = Category.objects.get(name=cat_name)
    except Category.DoesNotExist:
        print(f'  [SKIP] Category "{cat_name}" not found')
        continue

    if Product.objects.filter(name=item['name'], category=cat).exists():
        print(f'  [EXISTS] {item["name"]}')
        continue

    download(item['image_url'], item['image_file'])

    p = Product.objects.create(
        name=item['name'],
        category=cat,
        weight=item['weight'],
        mrp=item['mrp'],
        selling_price=item['selling_price'],
        is_hot_deal=True,
        image=item['image_file'],
    )
    print(f'  [ADDED] {item["name"]} - Rs.{item["mrp"]} -> Rs.{item["selling_price"]} ({p.discount_percentage()}% OFF)')


# ============================================================
# Summary
# ============================================================
print('\n' + '=' * 55)
hot = Product.objects.filter(is_hot_deal=True)
print(f'  Total Hot Deals: {hot.count()}')
print(f'  Total Products:  {Product.objects.count()}')
print('=' * 55)
print('\n  All Hot Deals:')
for p in hot.order_by('-mrp'):
    print(f'    {p.name:30s} Rs.{p.mrp} -> Rs.{p.selling_price} ({p.discount_percentage()}% OFF)')
