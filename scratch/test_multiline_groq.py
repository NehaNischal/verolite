import urllib.request
import urllib.parse
import json

SANITY_PROJECT_ID = '5nckxq6b'
SANITY_DATASET = 'production'
currentCat = 'recessed-led-down-lights'
filename = 'recessed-led-down-lights'

multiline_groq = f"""*[_type == "product" && !(_id in path("drafts.**")) && (
        category == "{currentCat}" || 
        category == "{filename}" || 
        category->slug.current == "{currentCat}" || 
        category->slug.current == "{filename}" ||
        categorySlug == "{currentCat}" ||
        categorySlug == "{filename}"
    )] | order(name asc){{
        _id,
        name,
        model,
        "slug": slug.current,
        "imageUrl": mainImage.asset->url,
        "category": coalesce(category->slug.current, category, categorySlug)
    }}"""

encoded = urllib.parse.quote(multiline_groq)
url = f'https://{SANITY_PROJECT_ID}.api.sanity.io/v2023-08-01/data/query/{SANITY_DATASET}?query={encoded}'

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        print("Success, count:", len(data.get('result', [])))
except urllib.error.HTTPError as e:
    print("HTTPError:", e.code, e.read().decode())
except Exception as e:
    print("Exception:", e)

