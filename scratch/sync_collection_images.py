import shutil

mapping = {
    "images/collection-1.jpg": "images/recessed-hero-banner.jpg",
    "images/collection-2.jpg": "images/surface-hero-banner.jpg",
    "images/collection-3.jpg": "images/track-hero-banner.jpg",
    "images/collection-4.jpg": "images/garden-hero-banner.jpg",
    "images/collection-5.jpg": "images/strip-hero-banner.jpg",
    "images/collection-6.jpg": "images/outdoor-hero-banner.jpg",
    "images/collection-7.jpg": "images/magnetic-hero-banner.jpg",
    "images/collection-8.jpg": "images/office-hero-banner.jpg",
    "images/collection-9.jpg": "images/drivers/driver-hero-banner.jpg",
    "images/collection-driver.jpg": "images/drivers/driver-hero-banner.jpg",
    "images/collection-10.jpg": "images/dimmer/dimmer-hero-banner.jpg",
    "images/collection-dimmer.jpg": "images/dimmer/dimmer-hero-banner.jpg",
    "images/collection-11.jpg": "images/sensors/sensor-hero-banner.jpg"
}

for dest, src in mapping.items():
    shutil.copy2(src, dest)
    print(f"Copied {src} -> {dest}")

print("All collection image files synchronized!")
