import re
import json
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class DocumentChunk:
    content: str
    metadata: Dict[str, Any]
    doc_type: str
    chunk_id: str


class DocumentParser:
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def parse_text(self, text: str, doc_type: str, source: str = "upload") -> List[DocumentChunk]:
        """Parse plain text into chunks"""
        chunks = []
        sentences = re.split(r'[.!?]+', text)

        current_chunk = ""
        chunk_id = 0

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            if len(current_chunk) + len(sentence) <= self.chunk_size:
                current_chunk += " " + sentence if current_chunk else sentence
            else:
                if current_chunk:
                    chunks.append(DocumentChunk(
                        content=current_chunk,
                        metadata={
                            "source": source,
                            "chunk_id": chunk_id,
                            "char_count": len(current_chunk)
                        },
                        doc_type=doc_type,
                        chunk_id=f"{source}_{chunk_id}"
                    ))
                    chunk_id += 1

                current_chunk = sentence

        if current_chunk:
            chunks.append(DocumentChunk(
                content=current_chunk,
                metadata={
                    "source": source,
                    "chunk_id": chunk_id,
                    "char_count": len(current_chunk)
                },
                doc_type=doc_type,
                chunk_id=f"{source}_{chunk_id}"
            ))

        return chunks

    def parse_pdf(self, file_path: str, doc_type: str = "pdf") -> List[DocumentChunk]:
        # TODO: Implement PDF parsing
        # For MVP, we'll handle text files and sample data
        pass