from dataclasses import dataclass, field
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
    id: int
    page_number: int
    filename: str
    text: str
    title: str = ""
    source: str = ""
    embedding: list[float] | None = None
    metadata: dict = field(default_factory=dict)

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