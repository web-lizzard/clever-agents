from pydantic import BaseModel


class DocumentMetadata(BaseModel):
    tokens: int
    headers: dict
    urls: list[str]
    images: list[str]
    context: str | None = None
    

class Document(BaseModel):
    text: str
    metadata: DocumentMetadata

