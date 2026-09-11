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

for html_file in html_files:
    path = os.path.join(workspace, html_file)
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # find cards
    # Let's find patterns like <div class="...card... or similar
    print(f"\n==================== {html_file} ====================")
    # find all images and surrounding text or headings
    headings = re.findall(r'<h[234][^>]*>(.*?)</h[234]>', content, re.IGNORECASE | re.DOTALL)
    cleaned_headings = [re.sub(r'<[^>]+>', '', h).strip() for h in headings]
    print("Headings:", [h for h in cleaned_headings if h and len(h) < 60][:15])
    
    # check if there is an array in script tag or static cards
    product_links = re.findall(r'href=[\'"]([^\'"]*product[^\'"]*)[\'"]', content, re.IGNORECASE)
    print("Product links:", product_links[:10])
