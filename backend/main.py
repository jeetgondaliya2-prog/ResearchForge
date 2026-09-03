import os
import json
from pathlib import Path
from datetime import datetime

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

# Load .env
from dotenv import load_dotenv
load_dotenv()

from backend.graph.workflow import build_graph
from backend.database.history import (
    save_research_result,
    get_history,
    get_research_by_id,
    delete_research_by_id,
    clear_history,
)

# ==========================================
# CONSTANTS
# ==========================================

UPLOAD_DIR = Path("data/uploads")
REPORTS_DIR = Path("generated_reports")

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# APP
# ==========================================

app = FastAPI(
    title="ResearchForge AI",
    description=(
        "Multi-Agent AI Research Platform powered by "
        "LangGraph, LangChain & Mistral AI"
    ),
    version="1.0.0",
)

# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# BUILD LANGGRAPH
# ==========================================

graph = build_graph()

# ==========================================
# SCHEMAS
# ==========================================

class ResearchRequest(BaseModel):
    user_query: str = ""
    query: str = ""   # alternate field name from some frontend versions


# ==========================================
# ROUTES — CORE
# ==========================================

@app.get("/")
def root():
    return {
        "message": "ResearchForge AI Backend is running",
        "status": "success",
        "version": "1.0.0",
        "agents": [
            "Supervisor", "Planner", "Web Researcher",
            "Academic Researcher", "RAG Researcher",
            "Research Merge", "Analyst", "Feasibility",
            "Critic", "Final Writer"
        ]
    }


@app.get("/health")
def health():
    return {"status": "healthy", "service": "ResearchForge AI"}


# ==========================================
# ROUTES — RESEARCH
# ==========================================

@app.post("/research")
def research(request: ResearchRequest):
    """
    Main research endpoint.
    Runs the full 10-agent LangGraph workflow and returns the final report.
    Accepts both `user_query` and `query` fields.
    """
    # Accept either field
    user_query = request.user_query or request.query

    if not user_query.strip():
        return {
            "status": "error",
            "message": "Please provide a research question (user_query)."
        }

    print(f"\n{'='*60}")
    print(f"NEW RESEARCH REQUEST")
    print(f"{'='*60}")
    print(f"Query: {user_query}")

    result = graph.invoke({
        "user_query": user_query,
        "revision_count": 0,
    })

    final_report = result.get("final_report", "")
    analysis = result.get("analysis", "")
    feasibility = result.get("feasibility", "")
    critique = result.get("critique", "")

    # Ensure feasibility is always a string (safety net)
    if isinstance(feasibility, dict):
        feasibility = feasibility.get("analysis", str(feasibility))

    print(f"\n[DONE] Research workflow completed.")

    # ── Save to history ──────────────────────────────────────
    saved = save_research_result(
        user_query=user_query,
        final_report=final_report,
        analysis=analysis,
        feasibility=feasibility,
        critique=critique,
    )

    # ── Save report to disk ───────────────────────────────────
    _save_report_to_disk(user_query, final_report)

    return {
        "status": "success",
        "user_query": user_query,
        "report": final_report,
        "final_report": final_report,
        "analysis": analysis,
        "feasibility": feasibility,
        "critique": critique,
        "history_id": saved.get("id", ""),
    }


def _save_report_to_disk(user_query: str, final_report: str) -> None:
    """Save the final report as a markdown file in generated_reports/."""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Sanitize query for filename
        safe_query = "".join(
            c if c.isalnum() or c in " _-" else "_"
            for c in user_query[:50]
        ).strip().replace(" ", "_")
        filename = REPORTS_DIR / f"{timestamp}_{safe_query}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# Research Report\n\n")
            f.write(f"**Query:** {user_query}\n\n")
            f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")
            f.write("---\n\n")
            f.write(final_report)
        print(f"[REPORT] Saved to: {filename}")
    except Exception as e:
        print(f"[REPORT] Could not save report: {e}")


# ==========================================
# ROUTES — RESEARCH HISTORY
# ==========================================

@app.get("/api/research/history")
def get_research_history(limit: int = 20):
    """Get the most recent research history entries."""
    history = get_history(limit=limit)
    return {
        "status": "success",
        "count": len(history),
        "history": history,
    }


@app.get("/api/research/history/{entry_id}")
def get_research_entry(entry_id: str):
    """Get a specific research entry by ID."""
    entry = get_research_by_id(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Research entry not found.")
    return {"status": "success", "entry": entry}


@app.delete("/api/research/history/{entry_id}")
def delete_research_entry(entry_id: str):
    """Delete a specific research entry by ID."""
    deleted = delete_research_by_id(entry_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Research entry not found.")
    return {"status": "success", "message": f"Deleted {entry_id}"}


@app.delete("/api/research/history")
def clear_research_history():
    """Clear all research history."""
    clear_history()
    return {"status": "success", "message": "History cleared."}


# ==========================================
# ROUTES — DOCUMENT UPLOAD & MANAGEMENT
# ==========================================

@app.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document (PDF/DOCX/TXT) for RAG processing.
    Saves it to data/uploads/ and triggers RAG ingestion.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided.")

    # Validate file type
    allowed_extensions = {".pdf", ".docx", ".txt", ".md"}
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{file_ext}' not supported. Allowed: {allowed_extensions}"
        )

    file_path = UPLOAD_DIR / file.filename
    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    print(f"[UPLOAD] Document saved: {file_path}")

    # Trigger RAG ingestion for uploaded file
    ingestion_status = _ingest_document(str(file_path))

    return {
        "status": "success",
        "message": f"Document '{file.filename}' uploaded successfully.",
        "filename": file.filename,
        "size_bytes": len(content),
        "ingestion": ingestion_status,
    }


def _ingest_document(file_path: str) -> str:
    """Ingest a document into the ChromaDB vector store."""
    try:
        from backend.rag.loaders import load_document
        from backend.rag.splitter import split_documents
        from backend.rag.vectorstore import get_vectorstore

        print(f"[INGEST] Loading document: {file_path}")
        docs = load_document(file_path)

        print(f"[INGEST] Splitting into chunks...")
        chunks = split_documents(docs)

        print(f"[INGEST] Storing {len(chunks)} chunks in ChromaDB...")
        vectorstore = get_vectorstore()
        vectorstore.add_documents(chunks)

        print(f"[INGEST] Ingestion complete.")
        return f"Ingested {len(chunks)} chunks successfully."

    except Exception as e:
        print(f"[INGEST] Ingestion failed: {e}")
        return f"Ingestion failed: {str(e)}"


@app.get("/api/documents/list")
def list_documents():
    """List all uploaded documents."""
    try:
        files = []
        for f in sorted(UPLOAD_DIR.iterdir()):
            if f.is_file() and not f.name.startswith("."):
                stat = f.stat()
                files.append({
                    "filename": f.name,
                    "size_bytes": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "extension": f.suffix.lower(),
                })
        return {"status": "success", "count": len(files), "documents": files}
    except Exception as e:
        return {"status": "error", "message": str(e), "documents": []}


@app.delete("/api/documents/{filename}")
def delete_document(filename: str):
    """Delete an uploaded document."""
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Document not found.")
    file_path.unlink()
    return {"status": "success", "message": f"Deleted {filename}"}


# ==========================================
# ROUTES — EXPORT
# ==========================================

@app.get("/api/export/reports")
def list_reports():
    """List all generated reports."""
    try:
        reports = []
        for f in sorted(REPORTS_DIR.iterdir(), reverse=True):
            if f.is_file() and f.suffix == ".md":
                stat = f.stat()
                reports.append({
                    "filename": f.name,
                    "size_bytes": stat.st_size,
                    "created": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                })
        return {"status": "success", "count": len(reports), "reports": reports}
    except Exception as e:
        return {"status": "error", "message": str(e), "reports": []}


@app.get("/api/export/reports/{filename}")
def download_report(filename: str):
    """Download a specific generated report."""
    file_path = REPORTS_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Report not found.")
    content = file_path.read_text(encoding="utf-8")
    return PlainTextResponse(content, media_type="text/markdown")


# ==========================================
# API PREFIX ALIASES (for frontend compatibility)
# ==========================================

@app.post("/api/research")
def api_research(request: ResearchRequest):
    return research(request)


@app.get("/api/health")
def api_health():
    return {"status": "healthy", "service": "ResearchForge AI"}