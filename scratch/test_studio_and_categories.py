import urllib.request

test_urls = [
    'http://localhost:3000/studio',
    'http://localhost:3000/studio/',
    'http://localhost:3000/studio/index.html',
    'http://localhost:3000/studio/structure',
    'http://localhost:3000/static/sanity-DumJ7oMy.js',
    'http://localhost:3000/static/sanity-lYNt0CIJ.css',
    'http://localhost:3000/office-linear-lights.html',
    'http://localhost:3000/3phase-track-lights.html',
    'http://localhost:3000/emergency-lights.html',
]

for u in test_urls:
    try:
        resp = urllib.request.urlopen(u, timeout=5)
        print(f"SUCCESS: {u} -> Status {resp.status}, Content-Type: {resp.headers.get('Content-Type')}")
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {u} -> Status {e.code}")
    except Exception as e:
        print(f"Error: {u} -> {e}")

