import glob
import re
import os

favicon_block = '''    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png">
    <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="512x512" href="favicon.png">
    <link rel="apple-touch-icon" sizes="180x180" href="favicon.png">
'''

html_files = sorted(glob.glob(r'c:\Users\user\Desktop\verolite\*.html'))
updated_files = []

for f in html_files:
    fname = os.path.basename(f)
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    
    # Clean up any stray character at very beginning (e.g. accidental 'e\n<!DOCTYPE html>')
    if content.startswith('e\n<!DOCTYPE html>') or content.startswith('e\r\n<!DOCTYPE html>'):
        content = re.sub(r'^e\r?\n', '', content)
    
    # Remove any existing favicon tags if any exist
    content = re.sub(r'[ \t]*<link[^>]*rel=["\'](?:shortcut\s+)?icon["\'][^>]*>\r?\n?', '', content, flags=re.IGNORECASE)
    content = re.sub(r'[ \t]*<link[^>]*rel=["\']apple-touch-icon["\'][^>]*>\r?\n?', '', content, flags=re.IGNORECASE)
    content = re.sub(r'[ \t]*<!-- Favicon -->\r?\n?', '', content)

    # Find the ideal insertion point: right after google-site-verification or robots meta
    inserted = False
    
    # Target 1: After google-site-verification meta tag
    gsv_pattern = re.compile(r'(<meta\s+name=["\']google-site-verification["\'][^>]*>)', re.IGNORECASE)
    if gsv_pattern.search(content):
        content = gsv_pattern.sub(r'\1\n' + favicon_block, content, count=1)
        inserted = True
    else:
        # Target 2: After <head>
        head_pattern = re.compile(r'(<head[^>]*>)', re.IGNORECASE)
        if head_pattern.search(content):
            content = head_pattern.sub(r'\1\n' + favicon_block, content, count=1)
            inserted = True

    if inserted:
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(content)
        updated_files.append(fname)
        print(f"Updated favicon in: {fname}")
    else:
        print(f"Failed to find insertion point in: {fname}")

print(f"\nTotal files updated: {len(updated_files)}")

