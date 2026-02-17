import os
import random
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Pillow library not found. Cannot generate images.")
    exit(1)

def create_placeholder(filename, text, size=(300, 300)):
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Random background color
    color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
    img = Image.new('RGB', size, color=color)
    
    d = ImageDraw.Draw(img)
    
    # Simple text centering (approximation as we might not have a font)
    # properly centering without a loaded font object is tricky, so we just put it consistently
    d.text((10, size[1]//2), text, fill=(255, 255, 255))
    
    img.save(filename)
    print(f"Generated {filename}")

images_to_generate = {
    'media/categories/fruit.png': 'Fruits',
    'media/categories/veg.png': 'Vegetables',
    'media/categories/dairy.png': 'Dairy',
    'media/categories/snacks.png': 'Snacks',
    'media/products/apple.png': 'Apple',
    'media/products/banana.png': 'Banana',
    'media/products/carrot.png': 'Carrot',
    'media/products/potato.png': 'Potato',
    'media/products/milk.png': 'Milk',
    'media/products/cheese.png': 'Cheese',
    'media/products/eggs.png': 'Eggs',
    'media/products/chips.png': 'Chips',
    'media/products/chocolate.png': 'Chocolate'
}

base_path = os.path.dirname(os.path.abspath(__file__))

for rel_path, text in images_to_generate.items():
    full_path = os.path.join(base_path, rel_path)
    if not os.path.exists(full_path):
        create_placeholder(full_path, text)
    else:
        print(f"Skipping {rel_path}, already exists.")
