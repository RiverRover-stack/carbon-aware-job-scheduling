from datetime import datetime, timedelta, timezone

from src.scheduler.evaluator import Job, JobStatus, select_jobs_for_dispatch


CURRENT_TIMESTAMP = datetime(2024, 1, 1, 12, tzinfo=timezone.utc)


def make_job(
    job_id: int,
    status: JobStatus = JobStatus.PENDING,
    start_by: datetime = CURRENT_TIMESTAMP + timedelta(hours=1),
) -> Job:
    return Job(
        job_id=job_id,
        job_name=f"job-{job_id}",
        status=status,
        start_by=start_by,
        duration=timedelta(minutes=30),
    )


def test_selects_pending_job_when_start_by_has_arrived():
    job = make_job(1, start_by=CURRENT_TIMESTAMP)

    selected = select_jobs_for_dispatch(
        [job],
        curr_carbon_intensity=200,
        current_timestamp=CURRENT_TIMESTAMP,
    )

    assert selected == [job]


def test_selects_pending_job_when_carbon_intensity_is_below_threshold():
    job = make_job(1)

    selected = select_jobs_for_dispatch(
        [job],
        curr_carbon_intensity=199,
        current_timestamp=CURRENT_TIMESTAMP,
    )

    assert selected == [job]


def test_does_not_select_pending_job_at_carbon_intensity_threshold_before_start_by():
    job = make_job(1)

    selected = select_jobs_for_dispatch(
        [job],
        curr_carbon_intensity=200,
        current_timestamp=CURRENT_TIMESTAMP,
    )

    assert selected == []


def test_does_not_select_jobs_that_are_not_pending():
    jobs = [
        make_job(1, status=JobStatus.RUNNING),
        make_job(2, status=JobStatus.DISPATCHED),
        make_job(3, status=JobStatus.COMPLETED),
        make_job(4, status=JobStatus.FAILED),
    ]

    selected = select_jobs_for_dispatch(
        jobs,
        curr_carbon_intensity=100,
        current_timestamp=CURRENT_TIMESTAMP,
    )

    assert selected == []


def test_preserves_input_order_and_does_not_change_job_status():
    jobs = [
        make_job(1, start_by=CURRENT_TIMESTAMP + timedelta(hours=1)),
        make_job(2, start_by=CURRENT_TIMESTAMP),
        make_job(3, start_by=CURRENT_TIMESTAMP + timedelta(hours=2)),
    ]

    selected = select_jobs_for_dispatch(
        jobs,
        curr_carbon_intensity=200,
        current_timestamp=CURRENT_TIMESTAMP,
    )

    assert selected == [jobs[1]]
    assert [job.status for job in jobs] == [
        JobStatus.PENDING,
        JobStatus.PENDING,
        JobStatus.PENDING,
    ]