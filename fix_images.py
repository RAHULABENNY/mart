"""Fix failed image downloads with alternative Unsplash URLs."""
import os, urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media')

FIXES = {
    'products/bread.png':      'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=300&h=300&fit=crop&q=80',
    'products/croissant.png':  'https://images.unsplash.com/photo-1530610476181-d83430b64dcd?w=300&h=300&fit=crop&q=80',
    'products/chilli.png':     'https://images.unsplash.com/photo-1583119022894-919a68a3d0e3?w=300&h=300&fit=crop&q=80',
    'products/tomato.png':     'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=300&h=300&fit=crop&q=80',
    'products/potato_new.png': 'https://images.unsplash.com/photo-1590165482129-1b8b27698780?w=300&h=300&fit=crop&q=80',
    'products/peanuts.png':    'https://images.unsplash.com/photo-1525351326368-efbb5cb6814d?w=300&h=300&fit=crop&q=80',
}

for rel, url in FIXES.items():
    full = os.path.join(BASE, rel)
    # Only download if missing or too small (placeholder)
    if os.path.exists(full) and os.path.getsize(full) > 2000:
        print(f"[SKIP] {rel} already good ({os.path.getsize(full)} bytes)")
        continue
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
            data = resp.read()
            with open(full, 'wb') as f:
                f.write(data)
        print(f"[OK]   {rel} ({len(data)} bytes)")
    except Exception as e:
        print(f"[FAIL] {rel}: {e}")
