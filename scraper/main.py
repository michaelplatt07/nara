from flask import Flask, request, Response, stream_with_context
import json
import time
from job import run_scrape_job
import threading
import uuid
import logging

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
    thread = threading.Thread(target=run_scrape_job, args=(job_id, recipe_url, jobs))
    thread.start()

    return {"job_id": job_id}, 201


@app.route("/jobs")
def list_jobs():
    return {
        "jobs": [{"id": key, "status": val["status"]} for key, val in jobs.items()]
    }, 200


@app.route("/jobs/<job_id>", methods=["DELETE"])
def delete_job(job_id: str):
    job = jobs.get(job_id)
    if not job:
        return {"error": "Invalid job ID"}, 400

    return {"job_id": job_id, "message": "Successfully deleted job"}, 204


@app.route("/jobs/<job_id>/status")
def get_job_status(job_id: str):
    logging.info(f"Fetching details for job: {job_id}")
    job = jobs.get(job_id)
    if not job:
        return {"error": "Invalid job ID"}, 400
    job_status = job.get("status")
    if job_status == "pending":
        return {"job_id": job_id, "status": job_status}, 200
    elif job_status == "error":
        return {
            "job_id": job_id,
            "status": job_status,
            "error": job.get("message"),
        }, 200
    else:
        return {
            "job_id": job_id,
            "status": job_status,
            "recipe": job.get("data"),
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
