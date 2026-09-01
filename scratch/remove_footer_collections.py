import glob
import re

html_files = glob.glob("*.html")

pattern = re.compile(r'\s*<!--\s*Col 3: Product Portfolio\s*-->\s*<div class="footer-col">\s*<h4 class="footer-heading">COLLECTIONS</h4>\s*<ul class="footer-links">[\s\S]*?</ul>\s*</div>', re.MULTILINE)

# Also alternative pattern without comments if any
pattern2 = re.compile(r'<div class="footer-col">\s*<h4 class="footer-heading">COLLECTIONS</h4>\s*<ul class="footer-links">[\s\S]*?</ul>\s*</div>', re.MULTILINE)

for hf in html_files:
    with open(hf, "r", encoding="utf-8") as f:
        content = f.read()
    
    new_content = pattern.sub('', content)
    if new_content == content:
        new_content = pattern2.sub('', content)
        
    if new_content != content:
        with open(hf, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Removed COLLECTIONS column from {hf}")
    else:
        print(f"No match for {hf}")
