"""
Download free demo images for categories and products from Unsplash.
Uses direct Unsplash source URLs which are free to use.
"""
import os
import urllib.request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, 'media')

# Unsplash source URLs - free to use, no API key needed
# Format: https://images.unsplash.com/photo-{id}?w={width}&h={height}&fit=crop
IMAGES = {
    # Category images (wider, banner-style)
    'categories/fruit.png': 'https://images.unsplash.com/photo-1619566636858-adf3ef46400b?w=400&h=300&fit=crop&q=80',
    'categories/veg.png': 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop&q=80',
    'categories/dairy.png': 'https://images.unsplash.com/photo-1628088062854-d1870b4553da?w=400&h=300&fit=crop&q=80',
    'categories/snacks.png': 'https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=400&h=300&fit=crop&q=80',

    # Product images (square, product-style)
    'products/apple.png': 'https://images.unsplash.com/photo-1584306670957-acf935f5033c?w=300&h=300&fit=crop&q=80',
    'products/banana.png': 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=300&h=300&fit=crop&q=80',
    'products/carrot.png': 'https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=300&h=300&fit=crop&q=80',
    'products/potato.png': 'https://images.unsplash.com/photo-1518977676601-b53f82ber9eb?w=300&h=300&fit=crop&q=80',
    'products/milk.png': 'https://images.unsplash.com/photo-1563636619-e9143da7973b?w=300&h=300&fit=crop&q=80',
    'products/cheese.png': 'https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?w=300&h=300&fit=crop&q=80',
    'products/eggs.png': 'https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=300&h=300&fit=crop&q=80',
    'products/chips.png': 'https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=300&h=300&fit=crop&q=80',
    'products/chocolate.png': 'https://images.unsplash.com/photo-1481391319762-47dff72954d9?w=300&h=300&fit=crop&q=80',
}

def download_images():
    print("Downloading demo images...")
    
    for rel_path, url in IMAGES.items():
        full_path = os.path.join(MEDIA_DIR, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        try:
            print(f"  Downloading {rel_path}...", end=' ')
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            with urllib.request.urlopen(req, timeout=15) as response:
                with open(full_path, 'wb') as f:
                    f.write(response.read())
            print("OK")
        except Exception as e:
            print(f"FAILED ({e})")

    print("\nDone! All images downloaded to media/ directory.")

if __name__ == '__main__':
    download_images()
