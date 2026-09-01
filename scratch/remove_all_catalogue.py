import glob
import re

html_files = glob.glob("*.html")

for fname in html_files:
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Remove Digital Catalogue li from footer
    new_content = re.sub(r'[ \t]*<li>\s*<a\s+href="[^"]*"\s+target="_blank">Digital Catalogue</a>\s*</li>\r?\n?', '', content)
    
    # 2. Also remove any remaining navbar or body CATALOGUE links
    new_content = re.sub(r'[ \t]*<a\s+href="[^"]*"\s+target="_blank">CATALOGUE</a>\r?\n?', '', new_content)
    new_content = re.sub(r'[ \t]*<a\s+href="[^"]*"\s+target="_blank">Catalogue</a>\r?\n?', '', new_content)
    
    # 3. In product.html, replace 'our catalog' with 'our collection'
    new_content = new_content.replace("in our catalog.", "in our collection.")
    
    if new_content != content:
        with open(fname, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Cleaned {fname}: Removed all Catalogue references.")
    else:
        print(f"No changes needed for {fname}")
