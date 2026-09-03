"""
Document loaders for ResearchForge AI RAG pipeline.
Supports PDF, DOCX, TXT and Markdown files.
"""

from pathlib import Path


def load_document(file_path: str):
    """
    Load a document from disk.
    Supports: .pdf, .docx, .txt, .md
    Returns a list of LangChain Document objects.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = path.suffix.lower()

    if ext == ".pdf":
        return _load_pdf(path)
    elif ext == ".docx":
        return _load_docx(path)
    elif ext in (".txt", ".md"):
        return _load_text(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def _load_pdf(path: Path):
    from langchain_community.document_loaders import PyPDFLoader
    loader = PyPDFLoader(str(path))
    return loader.load()


def _load_docx(path: Path):
    try:
        from langchain_community.document_loaders import Docx2txtLoader
        loader = Docx2txtLoader(str(path))
        return loader.load()
    except ImportError:
        # Fallback: read as plain text
        return _load_text(path)


def _load_text(path: Path):
    from langchain_core.documents import Document
    content = path.read_text(encoding="utf-8", errors="replace")
    return [Document(page_content=content, metadata={"source": str(path)})]


# ── Legacy alias for backward compatibility ─────────────────
def load_pdf(file_path: str):
    return _load_pdf(Path(file_path))