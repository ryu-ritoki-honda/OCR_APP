from dataclasses import dataclass
from typing import Optional
from utils.vector_store import VectorStore
from PIL import Image

@dataclass
class DocumentPage:
    page_number: int
    digital_text: str
    image: Image.Image
    processed_image: Image.Image | None = None
    ocr_text: str = ""
    merged_text: str = ""
    needs_ocr: bool = False

@dataclass
class Document:
    filename: str
    pages: list[DocumentPage]
    full_text: str = ""

@dataclass
class DocumentChunk:
    page_number: int
    chunk_id: int
    text: str
    embedding: list[float] | None = None

@dataclass
class PipelineResult:
    pages: list
    document: str
    chunks: list

@dataclass
class AppState:
    result: Optional[PipelineResult] = None
    vector_store: Optional[VectorStore] = None
    embeddings_generated: bool = False
    last_file_hash: Optional[str] = None