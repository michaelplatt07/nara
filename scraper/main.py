import json
import logging
import threading
import time
import uuid
from datetime import datetime

from flask import Flask, Response, request, stream_with_context
from job import run_scrape_job

from db import Job, get_job, get_jobs, insert_job, unset_fields, update_job

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


app = Flask(__name__)

# In memory storage of jobs running. This allows the process to be non-blocking and for the FE to poll for results
jobs = {}


@app.route("/health")
def health():
    return "Healthy", 201


@app.route("/scrape")
def scrape():
    recipe_url = request.args.get("recipe_url")
    if not recipe_url:
        logging.info("No URL provided")
        return "No URL provided", 500

    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "pending"}
    insert_job(
        Job(job_id=job_id, status="pending", created_at=datetime.now(), url=recipe_url)
    )
    thread = threading.Thread(target=run_scrape_job, args=(job_id, recipe_url, jobs))
    thread.start()

    return {"job_id": job_id}, 201


@app.route("/jobs")
def list_jobs():
    return {
        "jobs": [
            {
                "id": job["job_id"],
                "status": job["status"],
                "name": job.get("data", {}).get("name"),
                "url": job["url"],
            }
            for job in get_jobs()
        ]
    }, 200


@app.route("/jobs/<job_id>", methods=["DELETE"])
def delete_job(job_id: str):
    job = jobs.get(job_id)
    if not job:
        return {"error": "Invalid job ID"}, 400

    return {"job_id": job_id, "message": "Successfully deleted job"}, 204


@app.route("/jobs/<job_id>/retry")
def retry_job(job_id: str):
    job = get_job(Job(job_id=job_id))
    if not job:
        return {"error": "Invalid job ID"}, 400

    update_job(Job(job_id=job_id, status="pending"))
    unset_fields(Job(job_id=job_id, data=None, message=None))
    thread = threading.Thread(target=run_scrape_job, args=(job_id, job["url"], jobs))
    thread.start()

    return {"job_id": job_id}, 201


@app.route("/jobs/<job_id>/status")
def get_job_status(job_id: str):
    logging.info(f"Fetching details for job: {job_id}")

    # First check the immediate cache
    job = jobs.get(job_id)
    logging.info(f"Job from memory: {job}")

    # If not present, then check if the db has the job
    if not job:
        logging.info(f"No job in memory, searching DB with jobId: {job_id}")
        job = get_job(Job(job_id=job_id))
        logging.info(f"Job from db: {job}")

    # If still not present then the job never existed
    if not job:
        return {"error": "Invalid job ID"}, 400
    job_status = job.get("status")
    if job_status == "pending":
        return {"url": job.get("url"), "job_id": job_id, "status": job_status}, 200
    elif job_status == "error":
        return {
            "job_id": job_id,
            "status": job_status,
            "message": job.get("message"),
            "url": job.get("url"),
        }, 200
    else:
        return {
            "job_id": job_id,
            "status": job_status,
            "recipe": job.get("data"),
            "original_data": job.get("original_data"),
            "url": job.get("url"),
        }, 200


@app.route("/jobs/<job_id>/stream")
def get_job_stream(job_id: str):
    def generate():
        job = jobs.get(job_id)

        # Job not found
        if not job:
            yield f"data: {json.dumps({'status': 'not_found'})}"

        while job["status"] == "pending":
            job = jobs.get(job_id)

            # Push current status to client
            yield f"data: {job}\n\n"

            # If job is finished, close the stream
            if job["status"] in ["success", "error"]:
                break

            # Wait before checking again
            time.sleep(1)

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # important if using nginx
        },
    )
