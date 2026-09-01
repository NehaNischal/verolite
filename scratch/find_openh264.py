import urllib.request, json

req = urllib.request.Request("https://api.github.com/repos/cisco/openh264/releases/latest", headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print("Release tag:", data.get("tag_name"))
        for a in data.get("assets", []):
            print("Asset:", a.get("name"), a.get("browser_download_url"))
except Exception as e:
    print("Error:", e)
