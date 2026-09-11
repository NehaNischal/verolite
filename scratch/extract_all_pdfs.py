import fitz  # PyMuPDF
import os
import json

workspace = r"c:\Users\user\Desktop\verolite"
pdf_files = [f for f in os.listdir(workspace) if f.endswith('.pdf')]

extracted_data = {}

for pdf_name in pdf_files:
    pdf_path = os.path.join(workspace, pdf_name)
    print(f"\n==================== {pdf_name} ====================")
    doc = fitz.open(pdf_path)
    print(f"Total pages: {len(doc)}")
    
    extracted_data[pdf_name] = []
    
    for i, page in enumerate(doc):
        text = page.get_text().strip()
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        extracted_data[pdf_name].append({
            'page': i + 1,
            'text': text,
            'lines': lines
        })
        if text:
            print(f"--- Page {i+1} ---")
            print(text[:300].replace('\n', ' | '))

with open(os.path.join(workspace, 'scratch', 'extracted_pdf_text.json'), 'w', encoding='utf-8') as f:
    json.dump(extracted_data, f, indent=2, ensure_ascii=False)

print("\nFinished saving extracted PDF data to scratch/extracted_pdf_text.json")
