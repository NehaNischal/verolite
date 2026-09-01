import urllib.request
import bz2
import sys
import os

url = "http://ciscobinary.openh264.org/openh264-2.5.0-win64.dll.bz2"
dll_name = "openh264-2.5.0-win64.dll"
local_path = os.path.join(r"c:\Users\user\Desktop\verolite", dll_name)

print(f"Downloading {url}...")
try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        compressed_data = resp.read()
    print("Decompressing bz2...")
    decompressed_data = bz2.decompress(compressed_data)
    
    with open(local_path, "wb") as f:
        f.write(decompressed_data)
    print(f"Saved to {local_path} ({len(decompressed_data)} bytes)")
except Exception as e:
    print(f"Download error: {e}")
