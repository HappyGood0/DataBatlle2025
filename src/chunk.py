import os
from PyPDF2 import PdfReader, PdfWriter

# === Paramètres ===
pdf_path = "../Data/Official_Legal_Publications/case_law_of_the_boards_of_appeal_2022_en.pdf"
output_dir = "../Data/chunks"
num_chunks = 350       

# === Préparation ===
os.makedirs(output_dir, exist_ok=True)
reader = PdfReader(pdf_path)
total_pages = len(reader.pages)
chunk_size = total_pages // num_chunks

# === Division du PDF ===
for i in range(num_chunks):
    start = i * chunk_size
    end = (i + 1) * chunk_size if i < num_chunks - 1 else total_pages

    writer = PdfWriter()
    for page_num in range(start, end):
        writer.add_page(reader.pages[page_num])

    output_path = os.path.join(output_dir, f"law_text_{i+1:03}.pdf")
    with open(output_path, "wb") as f:
        writer.write(f)

    print(f"✅ Chunk {i+1:03} enregistré : {output_path}")

print(f"\n📚 Total : {num_chunks} fichiers enregistrés dans le dossier '{output_dir}'.")
