import re

pattern = re.compile(
    r'\s*<!-- Floating WhatsApp Widget -->\s*<div class="lumi-whatsapp-widget">[\s\S]*?</div>\s*(?=\s*<!-- Main Site Footer -->)',
    re.MULTILINE
)

files = [
    '3phase-track-lights.html',
    'led-garden-lights.html',
    'led-magnetic-track-lights.html',
    'led-phase-cut-dimmer.html',
    'led-sensor-switches.html',
    'led-strip-light-drivers.html',
    'recessed-led-down-lights.html'
]

for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    
    new_content, count = pattern.subn('\n\n    ', content)
    if count == 1:
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(new_content)
        print(f"Successfully updated {f}")
    else:
        print(f"Error in {f}: matched {count} times")
