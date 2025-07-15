# backend/main.py
from fastapi import FastAPI, HTTPException
from models import Job
from job_queue import enqueue_job, get_job_status

app = FastAPI()

@app.post("/jobs/submit")
def submit_job(job: Job):
    job_id = enqueue_job(job.dict())
    return {"job_id": job_id}

@app.get("/jobs/status/{job_id}")
def job_status(job_id: str):
    status = get_job_status(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return status
