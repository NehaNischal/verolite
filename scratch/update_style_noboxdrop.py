import glob

html_files = glob.glob("*.html")
for hf in html_files:
    with open(hf, "r", encoding="utf-8") as f:
        content = f.read()
    
    new_content = content.replace('href="style.css?v=sharp"', 'href="style.css?v=noboxdrop"')
    new_content = new_content.replace('href="style.css"', 'href="style.css?v=noboxdrop"')
    
    if new_content != content:
        with open(hf, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated style.css to v=noboxdrop in {hf}")
