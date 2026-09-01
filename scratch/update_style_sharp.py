import glob

html_files = glob.glob("*.html")
for hf in html_files:
    with open(hf, "r", encoding="utf-8") as f:
        content = f.read()
    
    new_content = content.replace('href="style.css?v=nobox"', 'href="style.css?v=sharp"')
    new_content = new_content.replace('href="style.css"', 'href="style.css?v=sharp"')
    
    if new_content != content:
        with open(hf, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated style.css to v=sharp in {hf}")
