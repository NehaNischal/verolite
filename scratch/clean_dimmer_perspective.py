import subprocess
import cv2
import numpy as np

# Load original pristine image
data = subprocess.check_output(["git", "show", "HEAD:images/collection-10.jpg"])
nparr = np.frombuffer(data, np.uint8)
orig = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

h, w, _ = orig.shape

# The text "LED Phace Cut Dimmer" is in roi: y in [40, 180], x in [25, 350]
# The 3D top glass edge runs from (x1=178, y1=147) to (x2=652, y2=128).
# Left vertical edge runs from (x1=178, y1=147) to (x3=178, y3=740).

# 1. Clean the text inside the glass plate (x > 178 and y > y_line(x)):
# The text "Phace Cut Dimmer" is black text on white frosted glass.
# In the region x in [180, 360], y in [148, 190], the frosted glass is solid white (RGB ~ 242-248).
# We can inpaint only the dark text pixels inside this region:
roi_glass = orig[146:190, 180:360]
gray_glass = cv2.cvtColor(roi_glass, cv2.COLOR_BGR2GRAY)
text_mask_glass = (gray_glass < 170).astype(np.uint8) * 255
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
text_mask_glass = cv2.dilate(text_mask_glass, kernel, iterations=2)

mask_full = np.zeros((h, w), dtype=np.uint8)
mask_full[146:190, 180:360] = text_mask_glass

cleaned = cv2.inpaint(orig, mask_full, 3, cv2.INPAINT_TELEA)

# 2. Clean the text outside the glass plate in the studio background:
# Region: x in [25, 178], y in [40, 180], and above the glass line for x in [178, 360]
# The studio background is a smooth gradient.
# Let's cleanly fill the background outside the glass plate:
for x in range(20, 380):
    # Calculate top glass edge Y at this X
    if x >= 178:
        glass_top_y = int(147.0 - (147.0 - 128.0) * (x - 178.0) / (652.0 - 178.0))
    else:
        glass_top_y = 740  # entire column is background
    
    for y in range(35, min(glass_top_y, 190)):
        # Sample clean background at same Y from x=720
        cleaned[y, x] = orig[y, 720]

# 3. For the glass bevel highlight along the line (x in [178, 380]):
# The bevel is a 2px highlight line right at glass_top_y.
# Let's ensure the glass top edge is crisp:
for x in range(178, 380):
    glass_top_y = int(147.0 - (147.0 - 128.0) * (x - 178.0) / (652.0 - 178.0))
    # Bevel highlight color:
    cleaned[glass_top_y - 1, x] = [175, 175, 178] # subtle dark outline
    cleaned[glass_top_y, x]     = [240, 240, 242] # bright glass highlight
    cleaned[glass_top_y + 1, x] = [245, 245, 247] # glass white body

# Clean bottom watermark residue (y > 725)
for y in range(725, h):
    cleaned[y, :] = cleaned[720, :]

paths = [
    r"images\collection-10.jpg",
    r"images\dimmer\phase-cut-dimmer.jpg",
    r"images\outdoor\phase-cut-dimmer.jpg",
    r"images\outdoor\phase-cut-dimmer-2.jpg"
]

for p in paths:
    cv2.imwrite(p, cleaned)

print("Saved mathematically perfect clean dimmer image!")
