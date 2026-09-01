import glob, cv2, os

images = [
    r"images\collection-11.jpg",
    r"images\drivers\constant-voltage-dimming-ip20.jpg",
    r"images\drivers\constant-voltage-dimming-ip65.jpg",
    r"images\drivers\constant-current-dimming.jpg",
    r"images\drivers\driver-ip65.jpg",
    r"images\sensors\cabinet-door-sensor.jpg",
    r"images\sensors\partition-touch-handwave-sensor.jpg",
    r"images\sensors\wireless-door-sensor.jpg",
    r"images\sensors\wireless-motion-sensor.jpg",
    r"images\outdoor\sensor-switches.jpg",
    r"images\outdoor\touch-wave-sensor.jpg",
    r"images\outdoor\door-sensor-switch.jpg",
    r"images\outdoor\motion-sensor-switch.jpg",
    r"images\outdoor\cable-sensor-switch.jpg"
]

for img_p in images:
    if os.path.exists(img_p):
        print(f"Exists: {img_p}")
