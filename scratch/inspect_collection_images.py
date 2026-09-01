import glob, cv2, os

collection_images = sorted(glob.glob(r"c:\Users\user\Desktop\verolite\images\collection-*.jpg"))
print("Found collection images:", collection_images)

for img_path in collection_images:
    img = cv2.imread(img_path)
    if img is not None:
        h, w, _ = img.shape
        print(f"{os.path.basename(img_path)}: {w}x{h}")
