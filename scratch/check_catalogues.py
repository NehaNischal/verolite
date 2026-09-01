import glob
import re

html_files = glob.glob("*.html")
print(f"Found {len(html_files)} HTML files:")

for fname in html_files:
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()
    
    matches = re.findall(r'[^\n]*CATALOGUE[^\n]*', content)
    print(f"\n{fname}:")
    for m in matches:
        print("  ", m.strip())
