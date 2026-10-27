import glob
import re

files = glob.glob('*.html')
for f in sorted(files):
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    match = re.search(r'<div class="nav-dropdown">([\s\S]*?</div>\s*</div>)', c)
    if match:
        print(f"=== {f} ===")
        lines = match.group(0).splitlines()
        print("\n".join(lines[:6]))
        print(f"Total lines in dropdown: {len(lines)}")
