import urllib.request, urllib.parse, json

SANITY_PROJECT_ID = '5nckxq6b'
SANITY_DATASET = 'production'
slug = 'vero-oliv'
groq = f'*[_type == "product" && (slug.current == "{slug}" || lower(name) == "{slug}")][0]{{_id, name, model, "slug": slug.current, category, shortDescription, description, specifications, features, variants, "imageUrl": mainImage.asset->url, "galleryCount": count(gallery)}}'
encoded = urllib.parse.quote(groq)
url = f'https://{SANITY_PROJECT_ID}.apicdn.sanity.io/v2023-08-01/data/query/{SANITY_DATASET}?query={encoded}'

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())
    print(json.dumps(data.get('result'), indent=2))
