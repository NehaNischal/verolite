import os
import re

workspace = r"c:\Users\user\Desktop\verolite"
html_files = [
    'recessed-led-down-lights.html',
    'led-surface-down-lights.html',
    '3phase-track-lights.html',
    'led-garden-lights.html',
    'led-strip-lights.html',
    'led-outdoor-flexible-neon-light.html',
    'led-magnetic-track-lights.html',
    'office-linear-lights.html',
    'led-strip-light-drivers.html',
    'led-phase-cut-dimmer.html',
    'led-sensor-switches.html'
]

all_products = []

for html_file in html_files:
    path = os.path.join(workspace, html_file)
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    cat_slug = html_file.replace('.html', '')
    
    # Extract each ref-card block
    # Pattern to match <div class="ref-card"...> ... </div>
    card_pattern = re.findall(r'<div class="ref-card(?:[^"]*)">(.*?)</div>\s*</div>', content, re.DOTALL)
    
    category_products = []
    
    for block in card_pattern:
        img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\'](?:[^>]+alt=["\']([^"\']*)["\'])?', block)
        img_src = img_match.group(1) if img_match else ""
        img_alt = img_match.group(2) if (img_match and img_match.group(2)) else ""
        
        prefix_match = re.search(r'<span class="prefix">(.*?)</span>', block)
        prefix = prefix_match.group(1).strip() if prefix_match else "VERO"
        
        name_match = re.search(r'<span class="name">(.*?)</span>', block)
        name = name_match.group(1).strip() if name_match else ""
        
        link_text_match = re.search(r'<span class="link-text">(.*?)</span>', block)
        type_text = link_text_match.group(1).strip() if link_text_match else ""
        
        if not name and img_alt:
            name = img_alt.replace("VERO ", "").replace("Recessed LED Down Light", "").strip()
        
        if name or img_src:
            full_name = f"{prefix} {name}".strip() if prefix else name
            prod_obj = {
                'category': cat_slug,
                'name': full_name,
                'model': full_name,
                'slug': re.sub(r'[^a-z0-9]+', '-', full_name.lower()).strip('-'),
                'image': img_src,
                'type_text': type_text
            }
            category_products.append(prod_obj)
            all_products.append(prod_obj)
            
    print(f"=== {html_file} -> {len(category_products)} products ===")
    for p in category_products:
        print(f"   - {p['name']} | Img: {p['image']}")

print(f"\nTotal products found: {len(all_products)}")
