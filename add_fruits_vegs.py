"""
Add more fruits and vegetables with proper PNG images.
"""
import os, sys, urllib.request, ssl

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
        print(f'  [SKIP] {rel_path}')
        return True
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
            data = resp.read()
            with open(full, 'wb') as f:
                f.write(data)
        print(f'  [OK]   {rel_path} ({len(data)} bytes)')
        return True
    except Exception as e:
        print(f'  [FAIL] {rel_path}: {e}')
        return False


# ============================================================
# New Fruits
# ============================================================
NEW_FRUITS = [
    {
        'name': 'Pineapple',
        'weight': '1 Piece',
        'mrp': 60,
        'selling_price': 49,
        'is_hot_deal': True,
        'image_url': 'https://images.unsplash.com/photo-1550258987-190a2d41a8ba?w=300&h=300&fit=crop&q=80',
        'image_file': 'products/pineapple.png',
    },
    {
        'name': 'Strawberry',
        'weight': '200 g',
        'mrp': 120,
        'selling_price': 99,
        'is_hot_deal': True,
        'image_url': 'https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=300&h=300&fit=crop&q=80',
        'image_file': 'products/strawberry.png',
    },
    {
        'name': 'Papaya',
        'weight': '1 Piece',
        'mrp': 45,
        'selling_price': 38,
        'is_hot_deal': False,
        'image_url': 'https://images.unsplash.com/photo-1517282009859-f000ec3b26fe?w=300&h=300&fit=crop&q=80',
        'image_file': 'products/papaya.png',
    },
    {
        'name': 'Guava',
        'weight': '500 g',
        'mrp': 40,
        'selling_price': 32,
        'is_hot_deal': False,
        'image_url': 'https://images.unsplash.com/photo-1536511132770-e5058c7e8c46?w=300&h=300&fit=crop&q=80',
        'image_file': 'products/guava.png',
    },
    {
        'name': 'Dragon Fruit',
        'weight': '1 Piece',
        'mrp': 90,
        'selling_price': 75,
        'is_hot_deal': True,
        'image_url': 'https://images.unsplash.com/photo-1527325678964-54921661f888?w=300&h=300&fit=crop&q=80',
        'image_file': 'products/dragonfruit.png',
    },
    {
        'name': 'Lemon',
        'weight': '250 g',
        'mrp': 20,
        'selling_price': 15,
        'is_hot_deal': False,
        'image_url': 'https://images.unsplash.com/photo-1590502593747-42a996133562?w=300&h=300&fit=crop&q=80',
        'image_file': 'products/lemon.png',
    },
    {
        'name': 'Coconut',
        'weight': '1 Piece',
        'mrp': 35,
        'selling_price': 28,
        'is_hot_deal': False,
        'image_url': 'https://images.unsplash.com/photo-1580984969071-a8da8c4e4920?w=300&h=300&fit=crop&q=80',
        'image_file': 'products/coconut.png',
    },
]

# ============================================================
# New Vegetables
# ============================================================
NEW_VEGETABLES = [
    {
        'name': 'Spinach (Palak)',
        'weight': '250 g',
        'mrp': 25,
        'selling_price': 20,
        'is_hot_deal': False,
        'image_url': 'https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=300&h=300&fit=crop&q=80',
        'image_file': 'products/spinach.png',
    },
    {
        'name': 'Cauliflower',
        'weight': '1 Piece',
        'mrp': 35,
        'selling_price': 28,
        'is_hot_deal': False,
        'image_url': 'https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=300&h=300&fit=crop&q=80',
        'image_file': 'products/cauliflower.png',
    },
    {
        'name': 'Green Chilli',
        'weight': '100 g',
        'mrp': 15,
        'selling_price': 10,
        'is_hot_deal': False,
        'image_url': 'https://images.unsplash.com/photo-1588252303782-cb80119abd6d?w=300&h=300&fit=crop&q=80',
        'image_file': 'products/green_chilli.png',
    },
    {
        'name': 'Ginger',
        'weight': '100 g',
        'mrp': 25,
        'selling_price': 20,
        'is_hot_deal': False,
        'image_url': 'https://images.unsplash.com/photo-1615485500704-8e990f9900f7?w=300&h=300&fit=crop&q=80',
        'image_file': 'products/ginger.png',
    },
    {
        'name': 'Beetroot',
        'weight': '500 g',
        'mrp': 30,
        'selling_price': 25,
        'is_hot_deal': False,
        'image_url': 'https://images.unsplash.com/photo-1593105544559-ecb03bf76f82?w=300&h=300&fit=crop&q=80',
        'image_file': 'products/beetroot.png',
    },
    {
        'name': 'Cucumber',
        'weight': '500 g',
        'mrp': 20,
        'selling_price': 15,
        'is_hot_deal': False,
        'image_url': 'https://images.unsplash.com/photo-1449300079323-02e209d9d3a6?w=300&h=300&fit=crop&q=80',
        'image_file': 'products/cucumber.png',
    },
    {
        'name': 'Corn (Sweet)',
        'weight': '2 Piece',
        'mrp': 40,
        'selling_price': 30,
        'is_hot_deal': True,
        'image_url': 'https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=300&h=300&fit=crop&q=80',
        'image_file': 'products/corn.png',
    },
    {
        'name': 'Mushroom',
        'weight': '200 g',
        'mrp': 45,
        'selling_price': 38,
        'is_hot_deal': True,
        'image_url': 'https://images.unsplash.com/photo-1504545102780-26774c1bb073?w=300&h=300&fit=crop&q=80',
        'image_file': 'products/mushroom.png',
    },
]


def add_products(cat_name, products):
    cat = Category.objects.get(name=cat_name)
    print(f'\n--- {cat_name} ---')
    for p in products:
        if Product.objects.filter(name=p['name'], category=cat).exists():
            print(f'  [EXISTS] {p["name"]}')
            continue
        download(p['image_url'], p['image_file'])
        Product.objects.create(
            name=p['name'],
            category=cat,
            weight=p['weight'],
            mrp=p['mrp'],
            selling_price=p['selling_price'],
            is_hot_deal=p.get('is_hot_deal', False),
            image=p['image_file'],
        )
        print(f'  [ADDED] {p["name"]} (Rs.{p["selling_price"]})')


if __name__ == '__main__':
    print('=' * 50)
    print('  Adding More Fruits & Vegetables')
    print('=' * 50)
    add_products('Fruits', NEW_FRUITS)
    add_products('Vegetables', NEW_VEGETABLES)
    print(f'\nTotal Fruits: {Product.objects.filter(category__name="Fruits").count()}')
    print(f'Total Vegetables: {Product.objects.filter(category__name="Vegetables").count()}')
    print(f'Total Products: {Product.objects.count()}')
