import json, re

path = r"C:\Users\user\.gemini\antigravity-ide\brain\f60bb9cd-7ee0-42e4-83c6-aed06201c81d\.system_generated\steps\25\content.md"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# find all .mp4 URLs
all_mp4 = set(re.findall(r'https?://[^\s"\'<>]+\.mp4[^\s"\'<>]*', text))
print("All MP4s found:", all_mp4)

# find story / video data
for m in re.finditer(r'("video_list"|"story_pin_data"|"videos"|"video_url"|"videoUrl"):(\{[^}]+\}|"[^"]+")', text):
    print("Match:", m.group(0)[:300])
