"""
Add products to every category, especially the empty and light ones.
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


def dl(url, rel):
    full = os.path.join(BASE, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    if os.path.exists(full) and os.path.getsize(full) > 2000:
        return
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
            d = r.read()
            with open(full, 'wb') as f:
                f.write(d)
    except:
        pass


DATA = {
    'soap': [
        {'name': 'Dove Beauty Bar', 'weight': '100 g', 'mrp': 65, 'selling_price': 55, 'is_hot_deal': True,
         'url': 'https://images.unsplash.com/photo-1600857544200-b2f666a9a2ec?w=300&h=300&fit=crop&q=80', 'img': 'products/dove_soap.png'},
        {'name': 'Dettol Original Soap', 'weight': '75 g', 'mrp': 42, 'selling_price': 35, 'is_hot_deal': False,
         'url': 'https://images.unsplash.com/photo-1584305574647-0cc949a2bb9f?w=300&h=300&fit=crop&q=80', 'img': 'products/dettol_soap.png'},
        {'name': 'Lux Soft Glow', 'weight': '100 g', 'mrp': 48, 'selling_price': 39, 'is_hot_deal': False,
         'url': 'https://images.unsplash.com/photo-1607006344380-b6775a0824a7?w=300&h=300&fit=crop&q=80', 'img': 'products/lux_soap.png'},
        {'name': 'Pears Pure & Gentle', 'weight': '125 g', 'mrp': 72, 'selling_price': 60, 'is_hot_deal': True,
         'url': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=300&h=300&fit=crop&q=80', 'img': 'products/pears_soap.png'},
        {'name': 'Himalaya Neem Soap', 'weight': '75 g', 'mrp': 40, 'selling_price': 32, 'is_hot_deal': False,
         'url': 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=300&h=300&fit=crop&q=80', 'img': 'products/neem_soap.png'},
    ],
    'liquid': [
        {'name': 'Vim Dishwash Liquid', 'weight': '500 ml', 'mrp': 99, 'selling_price': 79, 'is_hot_deal': True,
         'url': 'https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=300&h=300&fit=crop&q=80', 'img': 'products/vim_liquid.png'},
        {'name': 'Harpic Toilet Cleaner', 'weight': '500 ml', 'mrp': 110, 'selling_price': 89, 'is_hot_deal': False,
         'url': 'https://images.unsplash.com/photo-1563453392212-326f5e854473?w=300&h=300&fit=crop&q=80', 'img': 'products/harpic.png'},
        {'name': 'Lizol Floor Cleaner', 'weight': '500 ml', 'mrp': 125, 'selling_price': 99, 'is_hot_deal': True,
         'url': 'https://images.unsplash.com/photo-1528740561666-dc2479dc08ab?w=300&h=300&fit=crop&q=80', 'img': 'products/lizol.png'},
        {'name': 'Surf Excel Liquid', 'weight': '1 L', 'mrp': 220, 'selling_price': 179, 'is_hot_deal': True,
         'url': 'https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=300&h=300&fit=crop&q=80', 'img': 'products/surf_liquid.png'},
        {'name': 'Hand Wash (Lifebuoy)', 'weight': '250 ml', 'mrp': 85, 'selling_price': 69, 'is_hot_deal': False,
         'url': 'https://images.unsplash.com/photo-1584949091598-c31daaaa4aa9?w=300&h=300&fit=crop&q=80', 'img': 'products/handwash.png'},
    ],
    'Gel': [
        {'name': 'Set Wet Hair Gel', 'weight': '100 ml', 'mrp': 99, 'selling_price': 79, 'is_hot_deal': True,
         'url': 'https://images.unsplash.com/photo-1597354984706-fac992d9306f?w=300&h=300&fit=crop&q=80', 'img': 'products/hair_gel.png'},
        {'name': 'Aloe Vera Gel', 'weight': '120 ml', 'mrp': 150, 'selling_price': 110, 'is_hot_deal': True,
         'url': 'https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=300&h=300&fit=crop&q=80', 'img': 'products/aloe_gel.png'},
        {'name': 'Shower Gel (Nivea)', 'weight': '250 ml', 'mrp': 199, 'selling_price': 149, 'is_hot_deal': False,
         'url': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=300&h=300&fit=crop&q=80', 'img': 'products/shower_gel.png'},
        {'name': 'Face Wash Gel', 'weight': '100 ml', 'mrp': 175, 'selling_price': 135, 'is_hot_deal': False,
         'url': 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=300&h=300&fit=crop&q=80', 'img': 'products/face_wash.png'},
    ],
    'oils': [
        {'name': 'Coconut Oil', 'weight': '500 ml', 'mrp': 130, 'selling_price': 99, 'is_hot_deal': True,
         'url': 'https://images.unsplash.com/photo-1526947425960-945c6e72858f?w=300&h=300&fit=crop&q=80', 'img': 'products/coconut_oil.png'},
        {'name': 'Mustard Oil', 'weight': '1 L', 'mrp': 180, 'selling_price': 149, 'is_hot_deal': False,
         'url': 'https://images.unsplash.com/photo-1612540139150-4e678e4b8623?w=300&h=300&fit=crop&q=80', 'img': 'products/mustard_oil.png'},
        {'name': 'Groundnut Oil', 'weight': '1 L', 'mrp': 210, 'selling_price': 175, 'is_hot_deal': False,
         'url': 'https://images.unsplash.com/photo-1610725664285-7c57e6eeac3f?w=300&h=300&fit=crop&q=80', 'img': 'products/groundnut_oil.png'},
        {'name': 'Sesame Oil (Gingelly)', 'weight': '500 ml', 'mrp': 160, 'selling_price': 129, 'is_hot_deal': True,
         'url': 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=300&h=300&fit=crop&q=80', 'img': 'products/sesame_oil.png'},
    ],
    'Rice': [
        {'name': 'Sona Masoori Rice', 'weight': '5 kg', 'mrp': 380, 'selling_price': 310, 'is_hot_deal': True,
         'url': 'https://images.unsplash.com/photo-1536304993881-460e32f50dc2?w=300&h=300&fit=crop&q=80', 'img': 'products/sona_rice.png'},
        {'name': 'Brown Rice', 'weight': '1 kg', 'mrp': 120, 'selling_price': 95, 'is_hot_deal': False,
         'url': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=300&h=300&fit=crop&q=80', 'img': 'products/brown_rice.png'},
        {'name': 'Idli Rice', 'weight': '5 kg', 'mrp': 350, 'selling_price': 289, 'is_hot_deal': False,
         'url': 'https://images.unsplash.com/photo-1594756202469-9ff9799b2e4e?w=300&h=300&fit=crop&q=80', 'img': 'products/idli_rice.png'},
        {'name': 'Poha (Flattened Rice)', 'weight': '500 g', 'mrp': 55, 'selling_price': 42, 'is_hot_deal': False,
         'url': 'https://images.unsplash.com/photo-1596560548464-f010549b84d7?w=300&h=300&fit=crop&q=80', 'img': 'products/poha.png'},
    ],
    'Dairy': [
        {'name': 'Cream (Fresh)', 'weight': '200 ml', 'mrp': 75, 'selling_price': 62, 'is_hot_deal': False,
         'url': 'https://images.unsplash.com/photo-1563636619-e9143da7973b?w=300&h=300&fit=crop&q=80', 'img': 'products/cream.png'},
        {'name': 'Ghee (Amul)', 'weight': '500 ml', 'mrp': 320, 'selling_price': 275, 'is_hot_deal': True,
         'url': 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=300&h=300&fit=crop&q=80', 'img': 'products/ghee.png'},
        {'name': 'Milkshake (Chocolate)', 'weight': '200 ml', 'mrp': 40, 'selling_price': 30, 'is_hot_deal': True,
         'url': 'https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=300&h=300&fit=crop&q=80', 'img': 'products/milkshake.png'},
        {'name': 'Lassi (Sweet)', 'weight': '200 ml', 'mrp': 35, 'selling_price': 28, 'is_hot_deal': False,
         'url': 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=300&h=300&fit=crop&q=80', 'img': 'products/lassi.png'},
    ],
    'Beverages': [
        {'name': 'Coconut Water', 'weight': '200 ml', 'mrp': 30, 'selling_price': 25, 'is_hot_deal': False,
         'url': 'https://images.unsplash.com/photo-1536304929831-ee1ca9d44906?w=300&h=300&fit=crop&q=80', 'img': 'products/coconut_water.png'},
        {'name': 'Lemonade', 'weight': '300 ml', 'mrp': 25, 'selling_price': 20, 'is_hot_deal': False,
         'url': 'https://images.unsplash.com/photo-1621263764928-df1444c5e859?w=300&h=300&fit=crop&q=80', 'img': 'products/lemonade.png'},
        {'name': 'Lassi (Mango)', 'weight': '200 ml', 'mrp': 40, 'selling_price': 30, 'is_hot_deal': True,
         'url': 'https://images.unsplash.com/photo-1527661591475-527312dd65f5?w=300&h=300&fit=crop&q=80', 'img': 'products/mango_lassi.png'},
        {'name': 'Buttermilk (Chaas)', 'weight': '500 ml', 'mrp': 25, 'selling_price': 20, 'is_hot_deal': False,
         'url': 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=300&h=300&fit=crop&q=80', 'img': 'products/buttermilk.png'},
    ],
    'Bakery': [
        {'name': 'Pav Bun (Pack of 6)', 'weight': '300 g', 'mrp': 40, 'selling_price': 30, 'is_hot_deal': False,
         'url': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=300&h=300&fit=crop&q=80', 'img': 'products/pav_bun.png'},
        {'name': 'Cake (Vanilla)', 'weight': '500 g', 'mrp': 250, 'selling_price': 199, 'is_hot_deal': True,
         'url': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=300&h=300&fit=crop&q=80', 'img': 'products/vanilla_cake.png'},
        {'name': 'Rusk (Toast)', 'weight': '300 g', 'mrp': 45, 'selling_price': 35, 'is_hot_deal': False,
         'url': 'https://images.unsplash.com/photo-1619535860434-ba1d8fa12536?w=300&h=300&fit=crop&q=80', 'img': 'products/rusk.png'},
        {'name': 'Garlic Bread', 'weight': '200 g', 'mrp': 85, 'selling_price': 65, 'is_hot_deal': True,
         'url': 'https://images.unsplash.com/photo-1573140401552-3fab0b24306f?w=300&h=300&fit=crop&q=80', 'img': 'products/garlic_bread.png'},
    ],
    'Spices & Masala': [
        {'name': 'Cumin Seeds (Jeera)', 'weight': '100 g', 'mrp': 55, 'selling_price': 45, 'is_hot_deal': False,
         'url': 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=300&h=300&fit=crop&q=80', 'img': 'products/cumin.png'},
        {'name': 'Coriander Powder', 'weight': '100 g', 'mrp': 35, 'selling_price': 28, 'is_hot_deal': False,
         'url': 'https://images.unsplash.com/photo-1532336414038-cf19250c5757?w=300&h=300&fit=crop&q=80', 'img': 'products/coriander.png'},
        {'name': 'Black Pepper', 'weight': '50 g', 'mrp': 85, 'selling_price': 65, 'is_hot_deal': True,
         'url': 'https://images.unsplash.com/photo-1599639957043-f3aa5c986398?w=300&h=300&fit=crop&q=80', 'img': 'products/black_pepper.png'},
        {'name': 'Cinnamon Sticks', 'weight': '50 g', 'mrp': 60, 'selling_price': 48, 'is_hot_deal': False,
         'url': 'https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=300&h=300&fit=crop&q=80', 'img': 'products/cinnamon.png'},
        {'name': 'Mustard Seeds', 'weight': '100 g', 'mrp': 30, 'selling_price': 22, 'is_hot_deal': False,
         'url': 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=300&h=300&fit=crop&q=80', 'img': 'products/mustard_seeds.png'},
    ],
    'Snacks': [
        {'name': 'Mixture (Namkeen)', 'weight': '200 g', 'mrp': 55, 'selling_price': 42, 'is_hot_deal': False,
         'url': 'https://images.unsplash.com/photo-1599490659213-e2b9527bd087?w=300&h=300&fit=crop&q=80', 'img': 'products/mixture.png'},
        {'name': 'Banana Chips', 'weight': '200 g', 'mrp': 60, 'selling_price': 45, 'is_hot_deal': True,
         'url': 'https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=300&h=300&fit=crop&q=80', 'img': 'products/banana_chips.png'},
        {'name': 'Murukku', 'weight': '200 g', 'mrp': 70, 'selling_price': 55, 'is_hot_deal': False,
         'url': 'https://images.unsplash.com/photo-1604908177453-7462950a6a3b?w=300&h=300&fit=crop&q=80', 'img': 'products/murukku.png'},
    ],
}


def main():
    print('=' * 55)
    print('  Adding Products to Every Category')
    print('=' * 55)

    for cat_name, products in DATA.items():
        try:
            cat = Category.objects.get(name=cat_name)
        except Category.DoesNotExist:
            print(f'\n[SKIP] Category "{cat_name}" not found')
            continue

        print(f'\n--- {cat_name} ---')
        for p in products:
            if Product.objects.filter(name=p['name'], category=cat).exists():
                print(f'  [EXISTS] {p["name"]}')
                continue
            dl(p['url'], p['img'])
            Product.objects.create(
                name=p['name'], category=cat, weight=p['weight'],
                mrp=p['mrp'], selling_price=p['selling_price'],
                is_hot_deal=p['is_hot_deal'], image=p['img'],
            )
            print(f'  [ADDED] {p["name"]} Rs.{p["selling_price"]}')

    print('\n' + '=' * 55)
    print('  Summary')
    print('=' * 55)
    for c in Category.objects.all():
        count = Product.objects.filter(category=c).count()
        print(f'  {c.name:20s} {count} products')
    print(f'\n  Total: {Product.objects.count()} products')


if __name__ == '__main__':
    main()
