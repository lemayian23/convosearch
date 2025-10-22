import chromadb
from chromadb.config import Settings
from typing import List
import os
from .parser import DocumentChunk


class EmbeddingGenerator:
    def __init__(self):
        self.client = chromadb.HttpClient(
            host=os.getenv("CHROMA_HOST", "localhost"),
            port=os.getenv("CHROMA_PORT", "8001")
        )

    async def generate_embeddings(self, chunks: List[DocumentChunk], collection_name: str):
        """Generate embeddings and store in vector database"""
        collection = self.client.get_or_create_collection(collection_name)

        documents = []
        metadatas = []
        ids = []

        for chunk in chunks:
            documents.append(chunk.content)
            metadatas.append({
                "doc_type": chunk.doc_type,
                "source": chunk.metadata["source"],
                "chunk_id": chunk.chunk_id
            })
            ids.append(chunk.chunk_id)

        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

        print(f"Added {len(documents)} chunks to collection '{collection_name}'")