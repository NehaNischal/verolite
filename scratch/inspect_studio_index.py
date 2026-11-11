with open(r'c:\Users\user\Desktop\verolite\studio\index.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', c)
print('Script src paths:')
for s in scripts:
    print(' ', s)

links = re.findall(r'<link[^>]+href=["\']([^"\']+)["\']', c)
print('Link href paths:')
for l in links:
    print(' ', l)

