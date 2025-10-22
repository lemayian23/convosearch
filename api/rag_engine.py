import chromadb
from chromadb.config import Settings
import os
from typing import List, Dict, Any


class RAGEngine:
    def __init__(self):
        self.client = chromadb.HttpClient(
            host=os.getenv("CHROMA_HOST", "localhost"),
            port=os.getenv("CHROMA_PORT", "8001")
        )

    def query(self, question: str, collection_name: str = "faq", n_results: int = 3) -> Dict[str, Any]:
        """Query the vector database for relevant documents"""
        try:
            collection = self.client.get_collection(collection_name)

            results = collection.query(
                query_texts=[question],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )

            # Convert distances to confidence scores
            documents = results["documents"][0] if results["documents"] else []
            metadatas = results["metadatas"][0] if results["metadatas"] else []
            distances = results["distances"][0] if results["distances"] else []

            # Calculate confidence (inverse of distance, normalized)
            confidences = []
            for distance in distances:
                if distance is not None:
                    confidence = max(0, 1 - distance)  # Simple conversion
                    confidences.append(confidence)
                else:
                    confidences.append(0.5)

            sources = []
            for i, (doc, metadata) in enumerate(zip(documents, metadatas)):
                sources.append({
                    "content": doc,
                    "source": metadata.get("source", "unknown"),
                    "confidence": confidences[i] if i < len(confidences) else 0.5
                })

            return {
                "sources": sources,
                "average_confidence": sum(confidences) / len(confidences) if confidences else 0.5
            }

        except Exception as e:
            print(f"Error querying vector database: {e}")
            return {"sources": [], "average_confidence": 0.0}

    def get_relevant_context(self, question: str, collections: List[str] = None) -> List[str]:
        """Get relevant context from multiple collections"""
        if collections is None:
            collections = ["faq", "tickets"]

        all_sources = []
        for collection in collections:
            results = self.query(question, collection)
            all_sources.extend(results["sources"])

        # Sort by confidence and return top 3
        all_sources.sort(key=lambda x: x["confidence"], reverse=True)
        return [source["content"] for source in all_sources[:3]]