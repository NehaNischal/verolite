import urllib.request

urls = [
    'http://localhost:3000/studio/',
    'http://localhost:3000/emergency-lights.html',
    'http://localhost:3000/product.html?slug=emergency-exit-sign',
    'http://localhost:3000/index.html'
]

for url in urls:
    try:
        resp = urllib.request.urlopen(url, timeout=3)
        print(f"PASS: {url} -> Status {resp.status}, Content-Type: {resp.headers.get('Content-Type')}")
    except Exception as e:
        print(f"FAIL: {url} -> {e}")

