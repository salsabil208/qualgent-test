# backend/job_queue.py
import redis
import json
import time

r = redis.Redis(host='localhost', port=6379, db=0)

def enqueue_job(job_data):
    job_id = f"job-{r.incr('job_id_counter')}"
    # Add initial fields
    data = {"status": "queued", "created_at": time.time(), **job_data}
    r.set(job_id, json.dumps(data))
    # Use negative priority so higher priority comes first
    r.zadd(f"jobs:{job_data['app_version_id']}", {job_id: -job_data['priority']})
    return job_id

def get_job_status(job_id):
    job = r.get(job_id)
    if not job:
        return None
    return json.loads(job)

def pop_next_job(app_version_id):
    queue_name = f"jobs:{app_version_id}"
    # Get job with highest priority (zpopmax)
    job_tuple = r.zpopmax(queue_name)
    if not job_tuple or not job_tuple[0]:
        return None
    job_id = job_tuple[0][0].decode()
    return job_id

def get_all_app_version_queues():
    for key in r.scan_iter("jobs:*"):
        yield key.decode()
