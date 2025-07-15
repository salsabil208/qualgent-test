# worker.py
"""
Worker with prioritization, retries, and fault-tolerance for QualGent system.
"""

import redis
import json
import time
import random

MAX_RETRIES = 3
RUN_TIMEOUT = 30  # seconds

r = redis.Redis(host='localhost', port=6379, db=0)

def get_all_app_version_queues():
    for key in r.scan_iter("jobs:*"):
        yield key.decode()

def pop_next_job(app_version_id):
    queue_name = f"jobs:{app_version_id}"
    job_tuple = r.zpopmax(queue_name)
    if not job_tuple or not job_tuple[0]:
        return None
    job_id = job_tuple[0][0].decode()
    return job_id

def process_job(job_id, app_version_id):
    job_data_bytes = r.get(job_id)
    if not job_data_bytes:
        print(f"Job {job_id} disappeared from Redis!")
        return
    job_data = json.loads(job_data_bytes)

    # Mark as running with timestamp
    job_data['status'] = 'running'
    job_data['started_at'] = time.time()
    r.set(job_id, json.dumps(job_data))
    print(f"[Worker] Started {job_id}: {job_data}")

    time.sleep(2)  # Simulate work

    # Simulate random failure
    if random.random() < 0.2:
        job_data['retries'] = job_data.get('retries', 0) + 1
        if job_data['retries'] <= MAX_RETRIES:
            job_data['status'] = 'retrying'
            job_data['fail_reason'] = 'Simulated error, will retry'
            r.set(job_id, json.dumps(job_data))
            # Re-enqueue with same priority
            r.zadd(f"jobs:{app_version_id}", {job_id: -job_data['priority']})
            print(f"[Worker] RETRYING {job_id} (attempt {job_data['retries']})")
        else:
            job_data['status'] = 'failed'
            job_data['fail_reason'] = 'Max retries reached'
            r.set(job_id, json.dumps(job_data))
            print(f"[Worker] FAILED {job_id} (max retries)")
    else:
        job_data['status'] = 'done'
        job_data.pop('started_at', None)
        job_data.pop('fail_reason', None)
        r.set(job_id, json.dumps(job_data))
        print(f"[Worker] Finished {job_id}")

def requeue_stuck_jobs():
    """Requeue jobs that are stuck in 'running' state too long (fault-tolerance)"""
    for key in r.scan_iter("job-*"):
        job_data_bytes = r.get(key)
        if not job_data_bytes:
            continue
        job_data = json.loads(job_data_bytes)
        if job_data.get('status') == 'running':
            started_at = job_data.get('started_at', 0)
            if time.time() - started_at > RUN_TIMEOUT:
                job_data['status'] = 'retrying'
                job_data['fail_reason'] = 'Stuck in running, re-queued'
                job_data['retries'] = job_data.get('retries', 0) + 1
                r.set(key, json.dumps(job_data))
                app_version_id = job_data['app_version_id']
                r.zadd(f"jobs:{app_version_id}", {key.decode() if isinstance(key, bytes) else key: -job_data['priority']})
                print(f"[Worker] REQUEUED stuck job {key}")

def main():
    print("[Worker] Worker started, polling for jobs...")
    while True:
        found_job = False
        # Requeue stuck jobs for fault tolerance
        requeue_stuck_jobs()
        for queue_name in get_all_app_version_queues():
            app_version_id = queue_name.split(":")[1]
            job_id = pop_next_job(app_version_id)
            if job_id:
                process_job(job_id, app_version_id)
                found_job = True
        if not found_job:
            time.sleep(1)

if __name__ == "__main__":
    main()
