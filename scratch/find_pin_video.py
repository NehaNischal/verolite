import re
import json

path = r"C:\Users\user\.gemini\antigravity-ide\brain\f60bb9cd-7ee0-42e4-83c6-aed06201c81d\.system_generated\steps\25\content.md"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

print("File read, length:", len(text))

# Search for pin data json or video urls
mp4_urls = re.findall(r'https?://[^\s"\'<>]+\.mp4[^\s"\'<>]*', text)
print("MP4 URLs:", set(mp4_urls))

m3u8_urls = re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', text)
print("M3U8 URLs:", set(m3u8_urls))

pinimg_urls = re.findall(r'https?://v\.pinimg\.com/[^\s"\'<>]+', text)
print("v.pinimg URLs:", set(pinimg_urls))

# Search for video_list or story_pin_data or videos in JSON
scripts = re.findall(r'<script[^>]*>(.*?)</script>', text, re.DOTALL)
print("Found scripts:", len(scripts))
for i, s in enumerate(scripts):
    if "video" in s.lower():
        print(f"Script {i} contains video:")
        for line in s.split('\n'):
            if "video" in line.lower() or "mp4" in line.lower() or "720p" in line.lower() or "v.pinimg" in line:
                print("   ", line[:200])
