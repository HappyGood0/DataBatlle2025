from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import asyncio
import os

# Settings control global defaults
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
Settings.llm = Ollama(model="llama3.2", request_timeout=360.0)

# Create a RAG tool using LlamaIndex
documents = SimpleDirectoryReader("/home/cytech/Cours/DataBatlle2025/Data/Test").load_data()
index = VectorStoreIndex.from_documents(
    documents,
    # we can optionally override the embed_model here
    # embed_model=Settings.embed_model,
)
query_engine = index.as_query_engine(
    # we can optionally override the llm here
    # llm=Settings.llm,
)


async def search_documents(query: str) -> str:
    """Useful for answering natural language questions about an personal essay written by Paul Graham."""
    response = await query_engine.aquery(query)
    return str(response)


# Create an enhanced workflow with both tools
# agent = AgentWorkflow.from_tools_or_functions(
#     [search_documents],
#     llm=Settings.llm,
#     system_prompt="""Tyou aswear questions based on a given document""",
# )


# Now we can ask questions about the documents or do calculations
# async def main():
    # response = await agent.run(
    #     "How many questions are there in the document ?"
    # )
response = query_engine.query("What is 1234 *4567 ?")
print(response)


