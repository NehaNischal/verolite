import glob
import re
import os

favicon_block = '''    <!-- Favicon for all devices and sizes -->
    <link rel="icon" type="image/x-icon" href="favicon/favicon.ico">
    <link rel="icon" type="image/png" sizes="16x16" href="favicon/favicon-16x16.png">
    <link rel="icon" type="image/png" sizes="32x32" href="favicon/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="192x192" href="favicon/favicon-192x192.png">
    <link rel="icon" type="image/png" sizes="512x512" href="favicon/favicon.png">
    <link rel="apple-touch-icon" sizes="180x180" href="favicon/apple-touch-icon.png">
    <link rel="manifest" href="favicon/site.webmanifest">
'''

html_files = sorted(glob.glob(r'c:\Users\user\Desktop\verolite\*.html'))
updated_files = []

for f in html_files:
    fname = os.path.basename(f)
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    
    # Remove any existing favicon comments and links
    content = re.sub(r'[ \t]*<!-- Favicon.*?-->\r?\n?', '', content, flags=re.DOTALL)
    content = re.sub(r'[ \t]*<link[^>]*rel=["\'](?:shortcut\s+)?icon["\'][^>]*>\r?\n?', '', content, flags=re.IGNORECASE)
    content = re.sub(r'[ \t]*<link[^>]*rel=["\']apple-touch-icon["\'][^>]*>\r?\n?', '', content, flags=re.IGNORECASE)
    content = re.sub(r'[ \t]*<link[^>]*rel=["\']manifest["\'][^>]*>\r?\n?', '', content, flags=re.IGNORECASE)

    # Clean up any multiple blank lines
    content = re.sub(r'(\r?\n){3,}', '\n\n', content)

    # Insert right after google-site-verification or robots meta
    inserted = False
    gsv_pattern = re.compile(r'(<meta\s+name=["\']google-site-verification["\'][^>]*>)', re.IGNORECASE)
    if gsv_pattern.search(content):
        content = gsv_pattern.sub(r'\1\n' + favicon_block, content, count=1)
        inserted = True
    else:
        robots_pattern = re.compile(r'(<meta\s+name=["\']robots["\'][^>]*>)', re.IGNORECASE)
        if robots_pattern.search(content):
            content = robots_pattern.sub(r'\1\n' + favicon_block, content, count=1)
            inserted = True
        else:
            head_pattern = re.compile(r'(<head[^>]*>)', re.IGNORECASE)
            if head_pattern.search(content):
                content = head_pattern.sub(r'\1\n' + favicon_block, content, count=1)
                inserted = True

    if inserted:
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(content)
        updated_files.append(fname)
        print(f"Updated: {fname}")
    else:
        print(f"Failed to find insertion point: {fname}")

print(f"\nTotal files updated: {len(updated_files)}")

