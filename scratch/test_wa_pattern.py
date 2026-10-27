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
    matches = pattern.findall(content)
    print(f"{f}: {len(matches)} match(es)")
    if len(matches) > 0:
        print("MATCHED CONTENT:")
        print(repr(matches[0]))
