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
    ('reo', 'led-outdoor-flexible-neon-light.html'): 'vero-reo-neon',
    ('reo', 'office-linear-lights.html'): 'vero-reo-linear',
    ('magnetic track channel', 'led-magnetic-track-lights.html'): 'vero-magnetic-track-channel',
    ('led magnetic track channel', 'led-magnetic-track-lights.html'): 'vero-magnetic-track-channel',
    ('channel', 'led-magnetic-track-lights.html'): 'vero-magnetic-track-channel',
    ('phase cut dimmer', 'led-phase-cut-dimmer.html'): 'vero-phase-cut-dimmer',
    ('driver ip20', 'led-strip-light-drivers.html'): 'vero-driver-ip20',
    ('driver ip65', 'led-strip-light-drivers.html'): 'vero-driver-ip65',
    ('dimming driver ip65', 'led-strip-light-drivers.html'): 'vero-dimming-driver-ip65',
    ('dimming driver ip20', 'led-strip-light-drivers.html'): 'vero-dimming-driver-ip20',
    ('constant current dimming', 'led-strip-light-drivers.html'): 'vero-constant-current-dimming',
    ('cabinet door sensor', 'led-sensor-switches.html'): 'vero-cabinet-door-sensor',
    ('wireless motion sensor', 'led-sensor-switches.html'): 'vero-wireless-motion-sensor',
    ('wireless door sensor', 'led-sensor-switches.html'): 'vero-wireless-door-sensor',
    ('partition touch & hand wave', 'led-sensor-switches.html'): 'vero-partition-touch-hand-wave',
    ('partition touch & handwave', 'led-sensor-switches.html'): 'vero-partition-touch-hand-wave',
}

for filename in html_files:
    filepath = os.path.join(workspace, filename)
    if not os.path.exists(filepath):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Normalize any botched tags from earlier script:
    # Replace <a href="..." class="ref-card-link"> back to <div class="ref-card-link"> and clean trailing </a></div>
    content = re.sub(r'<a href="[^"]*" class="ref-card-link">', '<div class="ref-card-link">', content)
    content = re.sub(r'</div>\s*</a>\s*</div>', '</div>\n                    </div>\n                </a>', content)
    
    # Split content by card comments or structure
    # Match each full card block:
    # Starts with (<!-- \d+\. ... -->\s*)?<div class="ref-card"> or <a [^>]*class="ref-card">
    # Ends after the </div> that closes ref-card-info
    
    def process_card_match(m):
        comment = m.group(1) or ""
        img_src = m.group(2)
        img_alt = m.group(3) or ""
        prefix = m.group(4) or "VERO"
        name = m.group(5) or ""
        type_text = m.group(6) or "View Luminaire"
        
        raw_name = name.strip()
        key = (raw_name.lower(), filename)
        if key in CUSTOM_SLUGS:
            slug = CUSTOM_SLUGS[key]
        else:
            clean_name = re.sub(r'[^a-z0-9]+', '-', raw_name.lower()).strip('-')
            slug = f"vero-{clean_name}"
            
        return f'''{comment}<a href="product.html?slug={slug}" class="ref-card">
                    <div class="ref-card-img-box">
                        <img src="{img_src}" alt="{img_alt}" loading="lazy">
                    </div>
                    <div class="ref-card-info">
                        <div class="ref-card-title">
                            <span class="prefix">{prefix}</span>
                            <span class="name">{name}</span>
                        </div>
                        <div class="ref-card-link">
                            <span class="link-text">{type_text}</span>
                            <span class="link-arrow">&rarr;</span>
                        </div>
                    </div>
                </a>'''

    pattern = re.compile(
        r'(<!--\s*[\d\w\.\s\-_]+\s*-->\s*)?'
        r'<(?:div|a)[^>]*class="ref-card[^"]*"[^>]*>\s*'
        r'<div class="ref-card-img-box">\s*'
        r'<img[^>]+src=["\']([^"\']+)["\'][^>]*?(?:alt=["\']([^"\']*)["\'])?[^>]*?>\s*'
        r'</div>\s*'
        r'<div class="ref-card-info">\s*'
        r'<div class="ref-card-title">\s*'
        r'(?:<span class="prefix">([^<]*)</span>\s*)?'
        r'<span class="name">([^<]*)</span>\s*'
        r'</div>\s*'
        r'<(?:div|a)[^>]*class="ref-card-link">\s*'
        r'<span class="link-text">([^<]*)</span>\s*'
        r'<span class="link-arrow">[^<]*</span>\s*'
        r'</div>\s*'
        r'</div>\s*'
        r'</(?:div|a)>',
        re.DOTALL
    )

    new_content, count = pattern.subn(process_card_match, content)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"{filename}: processed {count} cards cleanly.")
