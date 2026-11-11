import urllib.request
import urllib.parse
import json

SANITY_PROJECT_ID = '5nckxq6b'
SANITY_DATASET = 'production'
groq = '*[_type == "product"]{_id, name, "catRef": category._ref, "catSlug": category->slug.current, categorySlug}'
url = f'https://{SANITY_PROJECT_ID}.api.sanity.io/v2023-08-01/data/query/{SANITY_DATASET}?query={urllib.parse.quote(groq)}'

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())
    products = data.get('result', [])
    print(f"Total products: {len(products)}")
    for p in products:
        print(f"  {p['name']:30} | ref={p.get('catRef')} | slug={p.get('catSlug')} | raw={p.get('categorySlug')}")

