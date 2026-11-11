import urllib.request
import urllib.parse
import json

SANITY_PROJECT_ID = '5nckxq6b'
SANITY_DATASET = 'production'

categories = [
    'recessed-led-down-lights',
    'led-surface-down-lights',
    '3phase-track-lights',
    'led-garden-lights',
    'led-strip-lights',
    'led-outdoor-flexible-neon-light',
    'led-magnetic-track-lights',
    'office-linear-lights',
    'led-strip-light-drivers',
    'led-phase-cut-dimmer',
    'led-sensor-switches',
    'emergency-lights'
]

print("Testing GROQ queries for each category:")
for cat in categories:
    currentCat = cat
    filename = cat
    groq = f'*[_type == "product" && !(_id in path("drafts.**")) && (category == "{currentCat}" || category == "{filename}" || category->slug.current == "{currentCat}" || category->slug.current == "{filename}" || categorySlug == "{currentCat}" || categorySlug == "{filename}")] | order(name asc){{_id, name, "slug": slug.current, "imageUrl": mainImage.asset->url, "category": coalesce(category->slug.current, category, categorySlug)}}'
    url = f'https://{SANITY_PROJECT_ID}.api.sanity.io/v2023-08-01/data/query/{SANITY_DATASET}?query={urllib.parse.quote(groq)}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            results = data.get('result', [])
            print(f"  {cat:32}: {len(results)} products found")
            if len(results) == 0:
                print(f"    --> ZERO PRODUCTS for {cat}!")
    except Exception as e:
        print(f"  {cat:32}: ERROR {e}")

