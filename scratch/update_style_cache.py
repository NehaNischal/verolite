import glob

html_files = glob.glob("*.html")
for hf in html_files:
    with open(hf, "r", encoding="utf-8") as f:
        content = f.read()
    
    new_content = content.replace('href="style.css"', 'href="style.css?v=nobox"')
    new_content = new_content.replace('href="style.css?v=final"', 'href="style.css?v=nobox"')
    new_content = new_content.replace('href="style.css?v=clean"', 'href="style.css?v=nobox"')
    
    if new_content != content:
        with open(hf, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated style.css cache buster in {hf}")
