import urllib.request
import urllib.parse
import json

SANITY_PROJECT_ID = '5nckxq6b'
SANITY_DATASET = 'production'

# 1. Query Category Groups
groq_groups = '*[_type == "categoryGroup"] | order(order asc){_id, title, "slug": slug.current, order}'
url_groups = f'https://{SANITY_PROJECT_ID}.api.sanity.io/v2023-08-01/data/query/{SANITY_DATASET}?query={urllib.parse.quote(groq_groups)}'

# 2. Query Subcategories with their parent group
groq_cats = '*[_type == "category"] | order(parentGroup->order asc, order asc){_id, title, "slug": slug.current, "parentGroup": parentGroup->title, pageUrl}'
url_cats = f'https://{SANITY_PROJECT_ID}.api.sanity.io/v2023-08-01/data/query/{SANITY_DATASET}?query={urllib.parse.quote(groq_cats)}'

# 3. Query sample products with their resolved category
groq_prods = '*[_type == "product"][0..5]{name, "categorySlug": coalesce(category->slug.current, category, categorySlug), "categoryTitle": coalesce(category->title, category), "parent": category->parentGroup->title}'
url_prods = f'https://{SANITY_PROJECT_ID}.api.sanity.io/v2023-08-01/data/query/{SANITY_DATASET}?query={urllib.parse.quote(groq_prods)}'

req_headers = {'User-Agent': 'Mozilla/5.0'}

print("--- PRIMARY CATEGORY GROUPS ---")
with urllib.request.urlopen(urllib.request.Request(url_groups, headers=req_headers)) as resp:
    data = json.loads(resp.read().decode())
    for g in data.get('result', []):
        print(f"  {g['order']}. {g['title']} (slug: {g['slug']})")

print("\n--- SUBCATEGORIES ---")
with urllib.request.urlopen(urllib.request.Request(url_cats, headers=req_headers)) as resp:
    data = json.loads(resp.read().decode())
    for c in data.get('result', []):
        print(f"  [{c.get('parentGroup')}] -> {c['title']} (slug: {c['slug']}, page: {c.get('pageUrl')})")

print("\n--- SAMPLE PRODUCTS ---")
with urllib.request.urlopen(urllib.request.Request(url_prods, headers=req_headers)) as resp:
    data = json.loads(resp.read().decode())
    for p in data.get('result', []):
        print(f"  {p['name']} -> {p['categoryTitle']} (slug: {p['categorySlug']}, parent: {p.get('parent')})")

