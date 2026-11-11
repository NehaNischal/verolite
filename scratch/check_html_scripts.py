import os
import glob
import re

for f in sorted(glob.glob(r'c:\Users\user\Desktop\verolite\*.html')):
    fname = os.path.basename(f)
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    scripts = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', c)
    has_grid = 'ref-products-grid' in c
    print(f"{fname:38}: grid={has_grid}, scripts={scripts}")

