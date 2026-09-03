from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.graph.workflow import build_graph


app = FastAPI(
    title="ResearchForge AI",
    description="Multi-Agent AI Research Assistant",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)


graph = build_graph()


class ResearchRequest(BaseModel):

    query: str


@app.get("/")
def home():

    return {
        "message": "ResearchForge AI API is running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/research")
def research(
    request: ResearchRequest
):

    result = graph.invoke(
        {
            "user_query": request.query,
            "revision_count": 0
        }
    )

    return {
        "query": request.query,
        "report": result.get(
            "final_report",
            ""
        )
    }


# API routes to match frontend calls
@app.post("/api/research")
def api_research(
    request: ResearchRequest
):
    """Research endpoint with /api prefix for frontend"""
    return research(request)


@app.post("/api/documents/upload")
def upload_document(file):
    """Document upload endpoint"""
    return {
        "message": "Document uploaded successfully",
        "filename": file.filename if file else None
    }


@app.get("/api/health")
def api_health():
    """Health check endpoint with /api prefix"""
    return {
        "status": "healthy",
        "service": "ResearchForge AI"
    }