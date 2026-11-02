import glob
import re
import os

html_files = glob.glob(r'c:\Users\user\Desktop\verolite\*.html')
print(f"Total HTML files found: {len(html_files)}")
found = 0
for f in html_files:
    filename = os.path.basename(f)
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    matches = re.findall(r'<link[^>]*rel=["\'][^"\']*icon[^"\']*["\'][^>]*>', c, re.IGNORECASE)
    if matches:
        print(f"{filename}: {matches}")
        found += 1

if found == 0:
    print("No existing icon links found in any HTML file.")

