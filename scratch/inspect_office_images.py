import glob, os, cv2

patterns = [
    r"c:\Users\user\Desktop\verolite\**\*.jpg",
    r"c:\Users\user\Desktop\verolite\**\*.png"
]

files = []
for pat in patterns:
    files.extend(glob.glob(pat, recursive=True))

for f in sorted(files):
    if "office" in f.lower() or "37" in f or "38" in f or "39" in f or "40" in f:
        try:
            img = cv2.imread(f)
            if img is not None:
                h, w, c = img.shape
                print(f"{f}: {w}x{h} ({os.path.getsize(f)} bytes)")
        except Exception as e:
            pass
