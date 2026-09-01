import glob
import re

html_files = glob.glob("*.html")

for fname in html_files:
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Remove VIEW LOOKBOOK button
    new_content = re.sub(r'[ \t]*<a\s+href="[^"]*"\s+class="btn-secondary">[\s\S]*?VIEW LOOKBOOK[\s\S]*?</a>\r?\n?', '', content)
    
    # 2. Remove footer-socials div and all its icons
    new_content = re.sub(r'[ \t]*<div class="footer-socials">[\s\S]*?</div>\r?\n?', '', new_content)
    
    # 3. Remove EXCLUSIVITY & INNOVATION subtitle
    new_content = re.sub(r'[ \t]*<span class="cta-subtitle">EXCLUSIVITY &amp; INNOVATION</span>\r?\n?', '', new_content)
    new_content = re.sub(r'[ \t]*<span class="cta-subtitle">EXCLUSIVITY & INNOVATION</span>\r?\n?', '', new_content)
    
    if new_content != content:
        with open(fname, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated {fname}: successfully removed requested elements.")
    else:
        print(f"No changes in {fname}")
