# backend/queue.py
import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

def enqueue_job(job_data):
    job_id = f"job-{r.incr('job_id_counter')}"
    r.set(job_id, json.dumps({"status": "queued", **job_data}))
    r.rpush(f"jobs:{job_data['app_version_id']}", job_id)
    return job_id

def get_job_status(job_id):
    job = r.get(job_id)
    if not job:
        return None
    return json.loads(job)
