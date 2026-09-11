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

# Map specific names to unique slugs
CUSTOM_SLUGS = {
    'reo': {
        'led-outdoor-flexible-neon-light.html': 'vero-reo-neon',
        'office-linear-lights.html': 'vero-reo-linear'
    },
    'magnetic track channel': {
        'led-magnetic-track-lights.html': 'vero-magnetic-track-channel'
    }
}

total_updated = 0

for filename in html_files:
    filepath = os.path.join(workspace, filename)
    if not os.path.exists(filepath):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all <div class="ref-card"...> ... </div> (matching the card container)
    # Let's replace each <div class="ref-card"> ... </div> with <a href="product.html?slug=..." class="ref-card"> ... </a>
    
    # We can use regex to find each card
    def replace_card(match):
        full_card = match.group(0)
        
        # Extract name
        name_match = re.search(r'<span class="name">(.*?)</span>', full_card)
        name = name_match.group(1).strip() if name_match else ""
        
        if not name:
            img_match = re.search(r'<img[^>]+alt=["\']([^"\']*)["\']', full_card)
            if img_match:
                name = img_match.group(1).replace("VERO ", "").replace("Recessed LED Down Light", "").strip()
        
        raw_key = name.lower()
        slug = None
        if raw_key in CUSTOM_SLUGS and filename in CUSTOM_SLUGS[raw_key]:
            slug = CUSTOM_SLUGS[raw_key][filename]
        elif name:
            slug = 'vero-' + re.sub(r'[^a-z0-9]+', '-', raw_key).strip('-')
        else:
            slug = 'vero-luminaire'

        # Replace outer <div class="ref-card"...> with <a href="product.html?slug=..." class="ref-card"...>
        # and closing </div> with </a>
        card_content = full_card
        card_content = re.sub(r'^<div\s+class="ref-card([^"]*)"', f'<a href="product.html?slug={slug}" class="ref-card\\1"', card_content)
        # replace the last closing </div> of this card with </a>
        card_content = re.sub(r'</div>\s*$', '</a>', card_content)
        return card_content

    # Regex for a ref-card
    new_content, count = re.subn(r'<div\s+class="ref-card[^"]*">(?:(?!<div\s+class="ref-card).)*?</div>\s*</div>', replace_card, content, flags=re.DOTALL)
    
    if count > 0:
        # Also ensure script.js version is bumped to bust cache
        new_content = re.sub(r'script\.js(\?v=[^"\'\s>]+)?', 'script.js?v=nav3', new_content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filename}: converted {count} cards to native <a> links")
        total_updated += count

print(f"\nTotal cards converted to direct links: {total_updated}")
