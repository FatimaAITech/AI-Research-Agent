import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.models import ResearchRequest, ResearchResponse
from services.research_service import ResearchService
from services.settings import settings


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