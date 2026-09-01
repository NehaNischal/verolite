import glob

html_files = glob.glob("*.html")
for hf in html_files:
    if hf == "contact.html":
        continue
    with open(hf, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace navbar and footer contact links
    new_content = content.replace('href="#contact">CONTACT US</a>', 'href="contact.html">CONTACT US</a>')
    new_content = new_content.replace('href="#contact">Contact Support</a>', 'href="contact.html">Contact Us</a>')
    new_content = new_content.replace('href="about.html#contact"', 'href="contact.html"')
    
    if new_content != content:
        with open(hf, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated contact links in {hf}")
