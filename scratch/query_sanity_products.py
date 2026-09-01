import urllib.request
import json

SANITY_PROJECT_ID = '5nckxq6b'
SANITY_DATASET = 'production'
groq = urllib.parse.quote('*[_type == "product"]{_id, name, model, "slug": slug.current, category, "imageUrl": mainImage.asset->url}')
url = f"https://{SANITY_PROJECT_ID}.apicdn.sanity.io/v2023-08-01/data/query/{SANITY_DATASET}?query={groq}"

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())
    print(json.dumps(data, indent=2))
