import urllib.request

origins_to_test = [
    'http://localhost:3000',
    'http://localhost:3333',
    'http://localhost:5173',
    'http://localhost:8000',
    'http://localhost:8080',
    'http://127.0.0.1:5500',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:8000',
    'http://localhost',
    'https://verolite.co.uk',
    'http://verolite.co.uk',
    'https://www.verolite.co.uk',
    'http://localhost:5000',
    'http://localhost:4000',
]

for origin in origins_to_test:
    req = urllib.request.Request(
        'https://5nckxq6b.api.sanity.io/v2023-08-01/data/query/production?query=*',
        headers={
            'Origin': origin,
            'User-Agent': 'Mozilla/5.0'
        }
    )
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"ALLOWED: {origin} (Status {resp.status})")
    except urllib.error.HTTPError as e:
        if e.code == 403:
            pass # forbidden cors
        else:
            print(f"{origin}: {e.code}")
    except Exception as e:
        print(f"{origin} error: {e}")
