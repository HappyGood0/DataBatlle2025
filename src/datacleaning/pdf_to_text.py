import fitz  
import os


pdf_dir = r"C:\Users\justi\Desktop\databattle\DataBatlle2025\Data\EPAC_Exams"
output_dir = r"C:\Users\justi\Desktop\databattle\DataBatlle2025\Data\EPAC_Exams txt"

# create the directoy if it does not exist
os.makedirs(output_dir, exist_ok=True)

# Looping through the folder
for filename in os.listdir(pdf_dir):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(pdf_dir, filename)
        output_txt = os.path.splitext(filename)[0] + ".txt"
        output_path = os.path.join(output_dir, output_txt)

        print(f"Processing: {filename}")
        doc = fitz.open(pdf_path)

        full_text = ""
        for page in doc:
            full_text += page.get_text()

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)

print("All PDFs converted to TXT successfully!")
