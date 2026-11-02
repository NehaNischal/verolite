import urllib.request
import urllib.parse
import json

SANITY_PROJECT_ID = '5nckxq6b'
SANITY_DATASET = 'production'

# 1. Query all categories in sanity to see what categories exist
groq_cats = '*[_type == "product"]{category, name, slug}'
endpoint_cats = f'https://{SANITY_PROJECT_ID}.api.sanity.io/v2023-08-01/data/query/{SANITY_DATASET}?query={urllib.parse.quote(groq_cats)}'

try:
    req = urllib.request.Request(endpoint_cats, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        products = data.get('result', [])
        print(f"Total products in Sanity: {len(products)}")
        categories = set(p.get('category') for p in products)
        print("Categories present in Sanity:", categories)
        for p in products:
            if 'emergency' in str(p).lower():
                print("Found emergency product:", p)
except Exception as e:
    print('Error:', e)
