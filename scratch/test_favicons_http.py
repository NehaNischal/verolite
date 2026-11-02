import urllib.request

urls = [
    'http://localhost:3000/favicon.ico',
    'http://localhost:3000/favicon.png',
    'http://localhost:3000/favicon-32x32.png',
    'http://localhost:3000/favicon-16x16.png',
    'http://localhost:3000/public/favicon.png',
    'http://localhost:3000/public/favicon.ico',
    'http://localhost:3000/index.html',
    'http://localhost:3000/product.html?slug=heli',
    'http://localhost:3000/emergency-lights.html'
]

for url in urls:
    try:
        resp = urllib.request.urlopen(url)
        print(f"PASS: {url} -> Status {resp.status}, Content-Type: {resp.headers.get('Content-Type')}, Size: {resp.headers.get('Content-Length')}")
    except Exception as e:
        print(f"FAIL: {url} -> {e}")

