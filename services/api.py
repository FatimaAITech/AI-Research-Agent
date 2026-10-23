import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.models import ResearchRequest, ResearchResponse
from services.research_service import ResearchService
from services.settings import settings


from pathlib import Path

from fastapi import HTTPException, Query

from memory.semantic_memory import SemanticMemory
from memory.memory_search import MemorySearch


from utils.file_handler import FileHandler
logger = logging.getLogger(__name__)

research_service = ResearchService()


app = FastAPI(
    title=settings.app_name,
    description="Production API for the AI Research Agent",
    version=settings.app_version,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    settings.frontend_url,
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
   ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service_ready": research_service.is_ready(),
    }


@app.get("/ready")
def ready():
    """
    Readiness check used by deployment platforms
    and container orchestration systems.
    """

    if not research_service.is_ready():
        return {
            "status": "not_ready",
            "service_ready": False,
        }

    return {
        "status": "ready",
        "service_ready": True,
    }


@app.post("/research", response_model=ResearchResponse)
def research(request: ResearchRequest):

    try:
        state = research_service.run(request.topic)

        report = state.final_report or state.report

        if not report:
            return ResearchResponse(
                success=False,
                topic=request.topic,
                error="Research completed but no report was generated.",
            )

        FileHandler.save_report(request.topic, report)

        return ResearchResponse(
            success=True,
            topic=request.topic,
            report=report,
        )

    except ValueError as e:
        return ResearchResponse(
            success=False,
            topic=request.topic,
            error=str(e),
        )

    except Exception:
        logger.exception(
            "Research execution failed for topic: %s",
            request.topic,
        )

        return ResearchResponse(
            success=False,
            topic=request.topic,
            error="Research execution failed. Please try again later.",
        )





REPORTS_DIR = Path("reports").resolve()


@app.get("/reports")
def list_reports():
    """Return saved Markdown research reports."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    reports = []
    for path in sorted(
        REPORTS_DIR.glob("*.md"),
        key=lambda item: item.stat().st_mtime,
        reverse=True,
    ):
        reports.append({
            "filename": path.name,
            "title": path.stem,
            "modified_at": path.stat().st_mtime,
        })

    return {"reports": reports}


@app.get("/reports/{filename}")
def get_report(filename: str):
    """Return the content of one saved report."""
    if (
        not filename.endswith(".md")
        or Path(filename).name != filename
        or "/" in filename
        or "\\" in filename
    ):
        raise HTTPException(status_code=400, detail="Invalid report filename.")

    path = (REPORTS_DIR / filename).resolve()

    if path.parent != REPORTS_DIR or not path.is_file():
        raise HTTPException(status_code=404, detail="Report not found.")

    return {
        "filename": path.name,
        "content": path.read_text(encoding="utf-8"),
    }


@app.get("/similar-topics")
def get_similar_topics(
    topic: str = Query(..., min_length=2, max_length=500)
):
    """Find related topics in existing research memory."""
    try:
        matches = SemanticMemory.search(topic, threshold=0.45)

        if not matches:
            matches = MemorySearch.search(topic, threshold=0.60)

        return {
            "query": topic,
            "matches": [
                {
                    "topic": item["topic"],
                    "score": item["score"],
                }
                for item in matches[:10]
            ],
        }
    except Exception:
        logger.exception("Similar-topic search failed.")
        raise HTTPException(
            status_code=503,
            detail="Research memory is temporarily unavailable.",
        )
