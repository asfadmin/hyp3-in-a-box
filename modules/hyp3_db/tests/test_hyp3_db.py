import pytest

from . import hyp3_db_test_utils as tu


@tu.run_if_creds
@tu.with_db
def test_db_creation(db):
    assert db is not None


@tu.run_if_creds
@tu.with_db
def test_get_enabled_subs(db):
    enabled_subs = db.get_enabled_subs()

    assert enabled_subs
    for sub in enabled_subs:
        assert sub.enabled is True


@tu.run_if_creds
@tu.with_db
def test_get_jobs(db):
    job_id = 2670
    job = db.get_job(job_id)

    assert job.id == job_id


@tu.run_if_creds
@tu.with_db
def test_set_job(db):
    job_id, new_status = 2670, 'QUEUED'

    job = db.get_job(job_id)
    old_status = job.status

    check_status(db, job, new_status)

    db.set_job_status(job, old_status)


def check_status(db, job, new_status):
    db.set_job_status(job, new_status)

    job_with_new_status = db.get_job(job.id)
    assert job_with_new_status.status == new_status


@tu.run_if_creds
@tu.with_db
def test_set_job_status_bad_status(db):
    job_id = 2670
    bad_status = 'blablabla'

    with pytest.raises(ValueError):
        db.set_job_status(
            job=job_id,
            status=bad_status
        )
