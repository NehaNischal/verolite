import cv2
import numpy as np

img = cv2.imread(r"images\collection-10.jpg")
h, w, _ = img.shape

# The glass plate top edge is a straight line at y ≈ 112 from x ≈ 170 to x ≈ 650.
# The left vertical edge is at x ≈ 170 from y ≈ 112 down to y ≈ 740.
# The background above the plate (y < 100) is a smooth vertical gradient:
# Let's inspect the background on the left (x < 150) and right (x > 670):

bg_left = img[:100, :150]
mean_bg = img[:100, :].mean(axis=(0,1))

# Let's clean the background region outside the plate:
# x < 165 and y < 700: background is smooth gradient
for y in range(0, 105):
    # Sample clean background from right side x in [700, 780]
    row_sample = img[y, 700:780].mean(axis=0)
    # Fill top-left background for x < 170
    img[y, :170] = row_sample

# Now let's draw the pristine glass top edge from x=170 to x=400:
# The glass edge on the right (x=380 to 650) has:
# A 2px highlight line at y=112, a 1px shadow at y=111, and the glass body below y=113.
# Let's clone the top edge from the right side (e.g. x=400 to 600) to x=175 to 375!
edge_template = img[105:140, 420:620]
img[105:140, 180:380] = edge_template

# And the top-left corner at (x=175, y=112)
# Clean the outer area above and to the left of the corner:
for y in range(0, 110):
    img[y, :180] = img[y, 700:780].mean(axis=0)

for x in range(0, 172):
    # Left background column matching y
    for y in range(0, h):
        if y < 700:
            img[y, x] = img[y, 0] # smooth column

# Save to all copies
paths = [
    r"images\collection-10.jpg",
    r"images\dimmer\phase-cut-dimmer.jpg",
    r"images\outdoor\phase-cut-dimmer.jpg",
    r"images\outdoor\phase-cut-dimmer-2.jpg"
]

for p in paths:
    cv2.imwrite(p, img)

print("Perfected dimmer images!")
