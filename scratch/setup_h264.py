import urllib.request
import bz2
import sys
import os

url = "https://github.com/cisco/openh264/releases/download/v2.5.0/openh264-2.5.0-win64.dll.bz2"
dll_name = "openh264-2.5.0-win64.dll"
py_dir = os.path.dirname(sys.executable)
target_path = os.path.join(py_dir, dll_name)
local_path = os.path.join(r"c:\Users\user\Desktop\verolite", dll_name)

print(f"Downloading {url}...")
try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        compressed_data = resp.read()
    print("Decompressing bz2...")
    decompressed_data = bz2.decompress(compressed_data)
    
    # Save to local path and python dir
    with open(local_path, "wb") as f:
        f.write(decompressed_data)
    print(f"Saved to {local_path}")
    
    try:
        with open(target_path, "wb") as f:
            f.write(decompressed_data)
        print(f"Saved to {target_path}")
    except Exception as e:
        print(f"Could not save to python dir: {e}")
except Exception as e:
    print(f"Download error: {e}")
