import pytest
import pathlib as pl

from hyp3_db import Hyp3DB


def creds_file_exists():
    creds_path = pl.Path(__file__).parent / '..' / 'hyp3_db' / 'creds.json'

    return creds_path.is_file()


run_if_creds = pytest.mark.skipif(
    not creds_file_exists(),
    reason='Test require database creds'
)


@run_if_creds
def test_get_enabled_subs():
    db = Hyp3DB()
    enabled_subs = db.get_enabled_subs()

    for sub in enabled_subs:
        assert sub.enabled is True


@run_if_creds
def test_get_jobs():
    job_id = 2670
    db = Hyp3DB()
    job = db.get_job(job_id)

    assert job.id == job_id


@run_if_creds
def test_set_job():
    job_id, new_status = 2670, 'QUEUED'
    db = Hyp3DB()

    job = db.get_job(job_id)
    old_status = job.status

    check_status(db, job, new_status)

    db.set_job_status(job, old_status)


def check_status(db, job, new_status):
    db.set_job_status(job, new_status)

    job_with_new_status = db.get_job(job.id)
    assert job_with_new_status.status == new_status


@run_if_creds
def test_set_job_status_bad_status():
    job_id = 2670
    db = Hyp3DB()
    bad_status = 'blablabla'

    with pytest.raises(ValueError):
        db.set_job_status(
            job=job_id,
            status=bad_status
        )
