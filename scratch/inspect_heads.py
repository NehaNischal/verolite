import glob
import os

html_files = sorted(glob.glob(r'c:\Users\user\Desktop\verolite\*.html'))
for f in html_files:
    fname = os.path.basename(f)
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        lines = fp.readlines()
    head_start = -1
    canonical_line = -1
    verification_line = -1
    for i, line in enumerate(lines[:35]):
        if '<head>' in line:
            head_start = i
        if 'rel="canonical"' in line:
            canonical_line = i
        if 'google-site-verification' in line:
            verification_line = i
    print(f"{fname:38}: head={head_start}, canonical={canonical_line}, verification={verification_line}")

