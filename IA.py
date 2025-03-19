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
    model_name="mistralai/Mistral-7B-Instruct-v0.1",
    api_key=hf_token,  # Correction : remplacer 'token' par 'api_key'
    request_timeout=360.0
)

# === Lecture du fichier PDF contenant le texte de loi ===
pdf_path = "data/case_law_of_the_boards_of_appeal_2022_en.pdf"
law_text = ""

with open(pdf_path, "rb") as f:
    reader = PyPDF2.PdfReader(f)
    for page in reader.pages:
        law_text += page.extract_text() or ""

print("Extracted text:", law_text[:500])  # Affiche les 500 premiers caractères du texte extrait


# === Création du prompt pour générer le quiz ===
prompt = f"""You are an expert legal quiz generator.
Based on the following law text, generate a quiz consisting of 5 multiple-choice questions.
For each question, provide:
- The question text.
- Four answer options labeled A, B, C, D.
- The correct answer (one of A, B, C, or D).
- A brief explanation for the correct answer.
"""

# Création d'un document à partir du texte complet
doc = Document(text=law_text)
documents = [doc]

# Création de l'index et du moteur de requêtes
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

async def generate_quiz() -> str:
    response = await query_engine.aquery(prompt)
    return str(response)

async def main():
    quiz = await generate_quiz()
    print("Generated Quiz:")
    print(quiz)

asyncio.run(main())