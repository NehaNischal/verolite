import glob, re

pages = [
    "recessed-led-down-lights.html",
    "led-surface-down-lights.html",
    "3phase-track-lights.html",
    "led-garden-lights.html",
    "led-strip-lights.html",
    "led-outdoor-flexible-neon-light.html",
    "led-magnetic-track-lights.html",
    "office-linear-lights.html",
    "led-strip-light-drivers.html",
    "led-phase-cut-dimmer.html",
    "led-sensor-switches.html"
]

for p in pages:
    try:
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Look for hero banner img or background image or category hero
        imgs = re.findall(r'<img[^>]+src="([^">]+)"', content)
        hero_imgs = [i for i in imgs if "hero" in i or "banner" in i or "collection" in i]
        print(f"=== {p} ===")
        print("Hero/Banner images:", hero_imgs)
        print("First 3 images on page:", imgs[:3])
    except Exception as e:
        print(f"Error {p}: {e}")
