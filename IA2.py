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

The format for the answers must be the following :
    - Question i (i being the actual number of the question) : The actual question

    - A) proposition A for the MCQ
    - B) proposition B for the MCQ
    - C) proposition C for the MCQ
    - D) proposition D for the mCQ

    - Correct answer : (put the letter of the right answer)

    - An explanation of why this is the correct answer

    -Source : The source where you found the answer (like the article number for example)

This is an example of the type of answers that I desire :
Question 4 : Which of the following is not a reason for excluding a mathematical method from patentability under Article 52(2) and (3) EPC 1973?

    A) The method is not a technical process.
    B) The method does not produce a direct technical result.
    C) The method is not carried out on a physical entity.
    D) The method is not described in mathematical terms.

Correct answer: D

Explanation: According to the text, a mathematical method or algorithm is carried out on numbers and provides a result also in numerical form. This means that the method is described in mathematical terms. Therefore, option D is not a reason for excluding a mathematical method from patentability under Article 52(2) and (3) EPC 1973.

Source : Article 52(2) and (3) EPC 1973.

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
