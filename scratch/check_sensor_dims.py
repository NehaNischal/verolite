import cv2

for fn in ["cabinet-door-sensor.jpg", "wireless-motion-sensor.jpg", "wireless-door-sensor.jpg", "partition-touch-handwave-sensor.jpg"]:
    img = cv2.imread(f"images/sensors/{fn}")
    h, w, _ = img.shape
    print(f"{fn}: {w}x{h}")
