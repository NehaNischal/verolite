import cv2

img = cv2.imread(r"images\garden-hero-banner.jpg")
h, w, _ = img.shape
print(f"garden-hero-banner.jpg: {w}x{h}")

# The fixture is on the right.
# Let's create a perfect square crop or composition where the full garden light fixture is centered and fully visible!
# In 1000x562 (or similar 16:9):
# The fixture + plant + light puddle can be composed into a beautiful 1:1 square:
# Let's crop x in [w - h - 50, w] or similar, ensuring 100% of the fixture and light beam is in frame.
