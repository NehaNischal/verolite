import urllib.request

urls = [
    'http://localhost:3000/favicon/favicon.ico',
    'http://localhost:3000/favicon/favicon-16x16.png',
    'http://localhost:3000/favicon/favicon-32x32.png',
    'http://localhost:3000/favicon/favicon-192x192.png',
    'http://localhost:3000/favicon/favicon.png',
    'http://localhost:3000/favicon/apple-touch-icon.png',
    'http://localhost:3000/favicon/site.webmanifest',
    'http://localhost:3000/favicon.ico',
    'http://localhost:3000/index.html',
    'http://localhost:3000/emergency-lights.html'
]

for url in urls:
    try:
        resp = urllib.request.urlopen(url, timeout=3)
        print(f"PASS: {url} -> Status {resp.status}, Content-Type: {resp.headers.get('Content-Type')}")
    except Exception as e:
        print(f"FAIL: {url} -> {e}")

