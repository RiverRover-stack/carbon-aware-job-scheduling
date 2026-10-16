from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum

class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    DISPATCHED = "dispatched"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Job:
    job_id: int
    job_name: str
    status: JobStatus
    start_by: datetime
    duration: timedelta
    creation_timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

def select_jobs_for_dispatch(list_of_jobs, curr_carbon_intensity, current_timestamp: datetime, carbon_intensity_threshold: int = 200):
    """
    Selects the jobs that are eligible for dispatching to the worker nodes based on their status and carbon intensity.
    It takes a list of jobs and dispatches it to the worker nodes.
    Output: A list of jobs that are dispatched to the worker nodes.
    """

    dispatched_jobs = []
    for job in list_of_jobs:
        if job.status == JobStatus.PENDING and (job.start_by <= current_timestamp or curr_carbon_intensity < carbon_intensity_threshold):  # This value will be fetched from the API or the cache
            # job.status = JobStatus.DISPATCHED
            dispatched_jobs.append(job)
    return dispatched_jobs

print("Job module loaded successfully.")