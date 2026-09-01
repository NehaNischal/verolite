import glob

html_files = glob.glob("*.html")
for hf in html_files:
    with open(hf, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Update recessed.css link with cache buster
    new_content = content.replace('href="recessed.css"', 'href="recessed.css?v=fresh3"')
    new_content = new_content.replace('href="recessed.css?v=fresh2"', 'href="recessed.css?v=fresh3"')
    new_content = new_content.replace('href="recessed.css?v=fresh"', 'href="recessed.css?v=fresh3"')
    
    if new_content != content:
        with open(hf, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated cache-buster in {hf}")
