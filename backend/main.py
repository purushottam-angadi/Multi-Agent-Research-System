from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid
import asyncio
from concurrent.futures import ThreadPoolExecutor

from pipeline import run_pipeline

app = FastAPI(
    title="AI Research Pipeline API",
    description="Multi-agent research pipeline powered by LangGraph + Mistral",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory job store  {job_id: {"status": ..., "result": ...}}
jobs: dict = {}
executor = ThreadPoolExecutor(max_workers=3)


class ResearchRequest(BaseModel):
    topic: str


class ResearchResponse(BaseModel):
    job_id: str
    status: str
    message: str


class ResearchResult(BaseModel):
    job_id: str
    status: str
    topic: Optional[str] = None
    report: Optional[str] = None
    feedback: Optional[str] = None
    citations: Optional[str] = None
    error: Optional[str] = None


def _run_pipeline_sync(job_id: str, topic: str):
    """Run pipeline in a thread and store result."""
    try:
        jobs[job_id]["status"] = "running"
        result = run_pipeline(topic)
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["result"] = result
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)


@app.get("/")
def root():
    return {"message": "Research Pipeline API is running 🚀", "docs": "/docs"}


@app.post("/research", response_model=ResearchResponse)
async def start_research(request: ResearchRequest, background_tasks: BackgroundTasks):
    """Start a research job. Returns a job_id to poll for results."""
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty.")

    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "queued", "result": None, "error": None}
    
    background_tasks.add_task(_run_pipeline_sync, job_id, request.topic.strip())



    return ResearchResponse(
        job_id=job_id,
        status="queued",
        message=f"Research job started. Poll /research/{job_id} for results.",
    )


@app.get("/research/{job_id}", response_model=ResearchResult)
def get_research_result(job_id: str):
    """Poll this endpoint to get job status and results."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found.")

    job = jobs[job_id]

    if job["status"] == "completed":
        return ResearchResult(
            job_id=job_id,
            status="completed",
            **job["result"],
        )
    elif job["status"] == "failed":
        return ResearchResult(
            job_id=job_id,
            status="failed",
            error=job.get("error", "Unknown error"),
        )
    else:
        return ResearchResult(
            job_id=job_id,
            status=job["status"],
        )


@app.get("/jobs")
def list_jobs():
    """List all jobs and their statuses."""
    return {
        jid: {"status": j["status"]}
        for jid, j in jobs.items()
    }
