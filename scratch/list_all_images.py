import glob, os

all_images = glob.glob(r"c:\Users\user\Desktop\verolite\images\**\*.jpg", recursive=True) + glob.glob(r"c:\Users\user\Desktop\verolite\images\**\*.png", recursive=True)
print(f"Total images found: {len(all_images)}")

for p in sorted(all_images):
    rel = os.path.relpath(p, r"c:\Users\user\Desktop\verolite")
    print(" ", rel)
