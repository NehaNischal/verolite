with open(r'c:\Users\user\Desktop\verolite\studio-verolite_sanity\scripts\import_all_products.ts', 'r', encoding='utf-8') as f:
    c = f.read()

import re
matches = re.findall(r'category:\s*[\'"]([^\'"]+)[\'"]', c)
from collections import Counter
counts = Counter(matches)
print("Products per category in import_all_products.ts:")
for cat, count in counts.items():
    print(f"  {cat:32}: {count}")

