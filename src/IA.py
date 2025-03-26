import os
import asyncio
import PyPDF2
from llama_index.core import VectorStoreIndex, Settings
from llama_index.llms.huggingface import HuggingFaceInferenceAPI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Document

# === Configuration des tokens API ===
hf_token = os.getenv("HF_TOKEN")# CA NE SERT A RIEN

# === Configuration des modèles via Hugging Face ===
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Utilisation de Mistral AI pour la génération via Hugging Face Inference API
Settings.llm = HuggingFaceInferenceAPI(
    max_tokens = 200000,
    model_name="mistralai/Mistral-7B-Instruct-v0.1",
    api_key=hf_token,  # Correction : remplacer 'token' par 'api_key'
    request_timeout=360.0
)

# === Lecture du fichier PDF contenant le texte de loi ===
pdf_path = "../Data/Official_Legal_Publications/case_law_of_the_boards_of_appeal_2022_en.pdf"
law_text = ""

with open(pdf_path, "rb") as f:
    reader = PyPDF2.PdfReader(f)
    for page in reader.pages:
        law_text += page.extract_text() or ""


# === Création du prompt pour générer le quiz ===
prompt = f"""You are an expert legal quiz generator.
Based on the following law text, generate a quiz consisting of 1 multiple-choice questions.
For each question, provide:
- The question text.
- Four answer options labeled A, B, C, D.
- The correct answer (one of A, B, C, or D).
- A brief explanation for the correct answer. You must alsocite title of the law article you used for the answer
"""

# Création d'un document à partir du texte complet
doc = Document(text=law_text)
documents = [doc]

# Création de l'index et du moteur de requêtes
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

async def generate_quiz() -> str:
    quiz = ""
    for i in range(0, 6):  # Générer 5 questions une par une
        response = await query_engine.aquery(prompt)
        quiz += str(response) + "\n\n"
    return quiz

async def main():
    quiz = await generate_quiz()
    with open("quiz_output.txt", "w", encoding="utf-8") as file:
        file.write(quiz)

asyncio.run(main())