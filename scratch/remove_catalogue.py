import glob
import re

html_files = glob.glob("*.html")

for fname in html_files:
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Match the navbar CATALOGUE anchor line (with any leading whitespace and newline)
    new_content = re.sub(r'[ \t]*<a\s+href="[^"]*"\s+target="_blank">CATALOGUE</a>\r?\n?', '', content)
    
    if new_content != content:
        with open(fname, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated {fname}: CATALOGUE removed from navbar.")
    else:
        print(f"No change in {fname}")
