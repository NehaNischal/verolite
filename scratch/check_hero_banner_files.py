import os

imgs = [
    "images/recessed-hero-banner.jpg",
    "images/surface-hero-banner.jpg",
    "images/track-hero-banner.jpg",
    "images/garden-hero-banner.jpg",
    "images/strip-hero-banner.jpg",
    "images/outdoor-hero-banner.jpg",
    "images/magnetic-hero-banner.jpg",
    "images/office-hero-banner.jpg",
    "images/drivers/driver-hero-banner.jpg",
    "images/dimmer/dimmer-hero-banner.jpg",
    "images/sensors/sensor-hero-banner.jpg"
]

for img in imgs:
    exists = os.path.exists(img)
    sz = os.path.getsize(img) if exists else 0
    print(f"{img}: exists={exists}, size={sz} bytes")
