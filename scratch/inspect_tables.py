import pdfplumber
import os
import json

workspace = r"c:\Users\user\Desktop\verolite"
pdf_files = [f for f in os.listdir(workspace) if f.endswith('.pdf')]

for pdf_name in pdf_files[:3]:
    pdf_path = os.path.join(workspace, pdf_name)
    print(f"\n==================== {pdf_name} ====================")
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            tables = page.extract_tables()
            print(f"--- Page {i+1} ---")
            print("Text:", text[:200] if text else "None")
            if tables:
                print("Tables found:", len(tables))
                for t in tables:
                    print("Table row 0:", t[0] if t else "Empty")
