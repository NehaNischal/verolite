import glob, os, cv2

all_imgs = sorted(glob.glob(r"images\**\*.jpg", recursive=True))
print(f"Checking {len(all_imgs)} images...")

for p in all_imgs:
    img = cv2.imread(p)
    if img is not None:
        h, w, _ = img.shape
        # Check top-left corner (first 25% height and width) for dark text if background is light
        tl = img[:int(h*0.25), :int(w*0.50)]
        gray = cv2.cvtColor(tl, cv2.COLOR_BGR2GRAY)
        dark_pixels = (gray < 80).sum()
        if dark_pixels > 200:
            print(f"Possible text in {p}: {dark_pixels} dark pixels in top-left region.")
