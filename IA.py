import os
import asyncio
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Récupération de la clé API OpenAI depuis les variables d'environnement
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("La clé API OpenAI n'est pas définie dans l'environnement.")

# Configuration des paramètres globaux avec OpenAI
Settings.embed_model = OpenAIEmbedding(api_key=openai_api_key)
Settings.llm = OpenAI(api_key=openai_api_key, model="text-davinci-003", request_timeout=360.0)

# Chargement des documents depuis le répertoire "documents"
documents = SimpleDirectoryReader("documents").load_data()

# Création de l'index et du moteur de requêtes
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

async def generate_questions() -> str:
    """
    Génère 5 questions logiques à partir du texte de loi.
    """
    prompt = (
        "Based on the provided law text, generate 5 logical and thought-provoking questions "
        "that a legal expert might ask."
    )
    response = await query_engine.aquery(prompt)
    return str(response)

async def main():
    questions = await generate_questions()
    print("Generated Questions:")
    print(questions)

asyncio.run(main())