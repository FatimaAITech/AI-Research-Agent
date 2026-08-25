from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from services.models import ResearchRequest, ResearchResponse
from services.research_service import ResearchService


app = FastAPI(
    title="AI Research Agent API",
    description="Production API for the AI Research Agent",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



logger = logging.getLogger(__name__)

research_service = ResearchService()


# -------------------------------------------------
# Root Endpoint
# -------------------------------------------------

@app.get("/")
def root():
    return {
        "name": "AI Research Agent API",
        "version": "1.0.0",
        "status": "running",
    }


# -------------------------------------------------
# Health Endpoint
# -------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service_ready": research_service.is_ready(),
    }


# -------------------------------------------------
# Research Endpoint
# -------------------------------------------------

@app.post("/research", response_model=ResearchResponse)
def research(request: ResearchRequest):

    try:

        state = research_service.run(
            request.topic
        )

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

    except Exception as e:

        logger.exception(
            "Research execution failed for topic: %s",
            request.topic,
        )

        return ResearchResponse(
            success=False,
            topic=request.topic,
            error="Research execution failed. Please try again later.",
        )