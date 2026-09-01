import urllib.request
import os

url = "https://v1.pinimg.com/videos/mc/720p/4b/fe/a6/4bfea62c2d1a982a4e17427ff6ef009b.mp4"
target_file = r"c:\Users\user\Desktop\verolite\hero-pinterest-video.mp4"

print(f"Downloading {url} to {target_file}...")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://in.pinterest.com/"
}

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp, open(target_file, "wb") as out:
    data = resp.read()
    out.write(data)

size = os.path.getsize(target_file)
print(f"Successfully downloaded {size} bytes ({size / (1024*1024):.2f} MB)")
