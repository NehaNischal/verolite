import glob
import re

files = sorted(glob.glob('*.html'))
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    c = re.sub(r'style\.css(?:\?[^"]*)?', 'style.css?v=mega1', c)
    c = re.sub(r'script\.js(?:\?[^"]*)?', 'script.js?v=mega1', c)
    with open(f, 'w', encoding='utf-8') as fp:
        fp.write(c)

print("Updated cache busting versions in all HTML files.")
