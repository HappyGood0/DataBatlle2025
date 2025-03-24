import os
import asyncio
import PyPDF2

from llama_index.core import VectorStoreIndex, Settings, Document
from llama_index.llms.huggingface import HuggingFaceInferenceAPI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# === Configuration de l'embedding et du LLM ===
hf_token = os.getenv("HF_TOKEN")  # Ton token HF ici si besoin

Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

Settings.llm = HuggingFaceInferenceAPI(
    model_name="mistralai/Mistral-7B-Instruct-v0.1",
    api_key=hf_token,
    request_timeout=360.0,
    max_tokens=2048
)

# === Prompt de génération ===
base_prompt = """You are an expert legal quiz generator.

Based on the following law text, generate a quiz consisting of 1 multiple-choice question.

For the question, provide:
- The question text.
- Four answer options labeled A, B, C, D.
- The correct answer (one of A, B, C, or D).
- A brief explanation for the correct answer. You must also cite the title of the law article you used for the answer.

Law text:
{chunk_text}
"""

# === Chemin vers les chunks ===
chunk_folder = "chunks"
start_chunk = 5
end_chunk = 335

async def generate_quiz_from_chunks():
    full_quiz = ""

    for i in range(start_chunk, end_chunk + 1):
        filename = os.path.join(chunk_folder, f"law_text_{i:03}.pdf")

        if not os.path.exists(filename):
            print(f"⚠️ Chunk {i:03} not found: {filename}")
            continue

        # Lire le texte du chunk PDF
        try:
            reader = PyPDF2.PdfReader(filename)
            chunk_text = ""
            for page in reader.pages:
                chunk_text += page.extract_text() or ""
        except Exception as e:
            print(f"❌ Erreur de lecture sur chunk {i:03} : {e}")
            continue

        if not chunk_text.strip():
            print(f"⛔ Chunk {i:03} est vide, ignoré.")
            continue

        # Créer un document et index temporaire
        document = Document(text=chunk_text)
        index = VectorStoreIndex.from_documents([document])
        query_engine = index.as_query_engine()

        # Générer la question
        prompt = base_prompt.format(chunk_text=chunk_text[:1500])  # Sécurité sur la longueur
        try:
            response = await query_engine.aquery(prompt)
            full_quiz += f"--- Question {i - start_chunk + 1} (Chunk {i:03}) ---\n{response}\n\n"
            print(f"✅ Généré pour chunk {i:03}")
        except Exception as e:
            print(f"❌ Erreur de génération sur chunk {i:03} : {e}")
            continue

    # Écriture du résultat
    with open("quiz_output.txt", "w", encoding="utf-8") as f:
        f.write(full_quiz)

    print("\n🎉 Génération terminée : quiz_output.txt")

# Lancer la génération
asyncio.run(generate_quiz_from_chunks())
