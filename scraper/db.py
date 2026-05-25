from datetime import datetime
from typing import NotRequired, TypedDict

from pymongo import MongoClient

uri = "mongodb://db:27017/"
client = MongoClient(uri)


class Job(TypedDict):
    job_id: str
    status: str
    created_at: datetime
    url: str
    original_data: NotRequired[str]
    data: NotRequired[dict]
    message: NotRequired[str]


def get_job(job: Job):
    try:
        db = client.get_database("dev")
        return db.jobs.find_one({"job_id": job["job_id"]})
    except Exception as e:
        raise Exception("Unable to fetch job") from e


def insert_job(job: Job):
    try:
        db = client.get_database("dev")
        db.jobs.insert_one(job)
    except Exception as e:
        raise Exception("Unable to insert job") from e


def update_job(job: Job):
    try:
        db = client.get_database("dev")
        fields = {key: value for key, value in job.items() if key != "job_id"}
        db.jobs.update_one({"job_id": job["job_id"]}, {"$set": fields})
    except Exception as e:
        raise Exception("Unable to update job") from e


def unset_fields(job: Job):
    try:
        db = client.get_database("dev")
        fields = {key: "" for key, value in job.items() if key != "job_id"}
        db.jobs.update_one({"job_id": job["job_id"]}, {"$unset": fields})
    except Exception as e:
        raise Exception("Unable to update job") from e


def get_jobs():
    try:
        db = client.get_database("dev")
        return db.jobs.find({}, {"job_id": 1, "status": 1, "url": 1, "data": 1}).sort(
            [("status", -1), ("created_at", -1)]
        )
    except Exception as e:
        raise Exception("Unable to get all jobs") from e
