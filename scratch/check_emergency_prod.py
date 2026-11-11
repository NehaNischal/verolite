import urllib.request
import urllib.parse
import json

SANITY_PROJECT_ID = '5nckxq6b'
SANITY_DATASET = 'production'
groq = '*[_type == "product" && (category._ref == "category-emergency-lights" || category->slug.current == "emergency-lights" || category == "emergency-lights")]{_id, name, model}'
url = f'https://{SANITY_PROJECT_ID}.api.sanity.io/v2023-08-01/data/query/{SANITY_DATASET}?query={urllib.parse.quote(groq)}'

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())
    print('Emergency products in Sanity:', data.get('result', []))

