import cv2

check_list = [
    r"images\collection-9.jpg",
    r"images\collection-10.jpg",
    r"images\collection-11.jpg",
    r"images\dimmer\phase-cut-dimmer.jpg",
    r"images\drivers\driver-ip20.jpg",
    r"images\outdoor\driver-ip20.jpg",
    r"images\outdoor\phase-cut-dimmer.jpg",
    r"images\outdoor\sensor-switches.jpg"
]

for p in check_list:
    img = cv2.imread(p)
    if img is not None:
        print(f"Loaded {p}: {img.shape}")
