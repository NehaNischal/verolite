import cv2
import numpy as np

img = cv2.imread(r"images\collection-10.jpg")
h, w, _ = img.shape

# In the top glass edge:
# Left corner is (x1=178, y1=147)
# Right corner is (x2=652, y2=128)
# Line slope: dy = (128 - 147) / (652 - 178) = -19 / 474 = -0.040084

# For x from 178 to 380 (the region where the text was):
# The top background (y < y_edge(x)) should be clean studio background.
# The glass panel body (y > y_edge(x) + 3) should be clean white glass (RGB: 246, 246, 247).
# The glass top edge (y == y_edge(x) to y_edge(x) + 3) should have the translucent bevel.

for x in range(178, 380):
    edge_y = 147.0 - 0.040084 * (x - 178.0)
    iy = int(np.round(edge_y))
    
    # Background above edge:
    for y in range(40, iy - 1):
        # sample clean background on the left at x=150
        img[y, x] = img[y, 150]
        
    # Edge bevel (3 pixels):
    img[iy - 1, x] = [178, 180, 182] # outer border
    img[iy, x]     = [220, 222, 224] # glass highlight
    img[iy + 1, x] = [238, 239, 240] # glass inner highlight
    
    # Glass body below bevel:
    for y in range(iy + 2, iy + 25):
        img[y, x] = [246, 247, 248]

# Left vertical edge from y=147 down to 220 at x=178:
# Outer border at x=177, highlight at x=178, inner glass at x=179
for y in range(147, 220):
    for x in range(40, 177):
        img[y, x] = img[y, 150]
    img[y, 176] = [180, 182, 184]
    img[y, 177] = [215, 217, 220]
    img[y, 178] = [242, 243, 245]

# Save to all copies
paths = [
    r"images\collection-10.jpg",
    r"images\dimmer\phase-cut-dimmer.jpg",
    r"images\outdoor\phase-cut-dimmer.jpg",
    r"images\outdoor\phase-cut-dimmer-2.jpg"
]

for p in paths:
    cv2.imwrite(p, img)

print("Saved razor sharp dimmer image!")
