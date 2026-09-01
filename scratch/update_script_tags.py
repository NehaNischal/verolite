import glob, re

files = glob.glob("*.html")
for f in files:
    with open(f, "r", encoding="utf-8") as file:
        content = file.read()
    new_content = re.sub(r'src="script\.js(?:\?[^"]*)?"', 'src="script.js?v=clean2"', content)
    if new_content != content:
        with open(f, "w", encoding="utf-8") as file:
            file.write(new_content)
        print(f"Updated {f} with script.js?v=clean2")
