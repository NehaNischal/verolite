import glob
import re

files = sorted(glob.glob('*.html'))
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    m = re.search(r'<div class="dropdown-menu">([\s\S]*?)</div>', c)
    if m:
        has_active = 'class="dropdown-item active"' in m.group(1) or 'active' in m.group(1)
        print(f"{f}: has active inside menu? {has_active}")
