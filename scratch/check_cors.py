import urllib.request

req = urllib.request.Request(
    'https://5nckxq6b.api.sanity.io/v2023-08-01/data/query/production?query=*',
    headers={
        'Origin': 'http://localhost:5500',
        'User-Agent': 'Mozilla/5.0'
    }
)

try:
    with urllib.request.urlopen(req) as resp:
        print("Status:", resp.status)
        print("CORS header:", resp.headers.get('Access-Control-Allow-Origin'))
except urllib.error.HTTPError as e:
    print("HTTPError:", e.code)
    print("CORS header:", e.headers.get('Access-Control-Allow-Origin'))
    print(e.read().decode())
except Exception as e:
    print("Error:", e)
