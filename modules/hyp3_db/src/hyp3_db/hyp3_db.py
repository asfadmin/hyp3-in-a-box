from sqlalchemy import sql

from .session import make_session
from .hyp3_models import Subscription, LocalQueue


class Hyp3DB:
    valid_job_status = [
        'INVALID',
        'INSERTED',
        'ERROR',
        'HOLD',
        'FAILED',
        'SUCCEEDED',
        'PROCESSING',
        'COMPLETE',
        'QUEUED',
        'CANCELLED'
    ]

    def __init__(self, host, user, password):
        self.session = make_session(host, user, password)

    def get_enabled_subs(self):
        subs = self.session                       \
            .query(Subscription)                  \
            .filter(Subscription.enabled == True) \
            .all()

        return subs

    def get_job(self, job_id):
        return self.session                       \
            .query(LocalQueue)               \
            .filter(LocalQueue.id == job_id) \
            .one()

    # TODO: Get user and process id from subscription
    def add_job(self, sub, granule, granule_url, message):
        user = 'sqlalchemy stuff here'
        process = 'sqlalchemy stuff here'
        new_job = LocalQueue(
            granule=granule,
            granule_url=granule_url,
            request_time=sql.func.now(),
            priority=5,
            sub_id=sub.id,
            user_id=user.id,
            process_id=process.id,
            status='QUEUED',
            message=message
        )

        self.session.add(new_job)
        return new_job

    def set_job_status(self, job, status):
        if status not in Hyp3DB.valid_job_status:
            raise ValueError(f'{status} not a valid job_status.')

        if isinstance(job, LocalQueue):
            job.status = status
        else:
            job_id = job
            self.session.query(LocalQueue) \
                .filter(LocalQueue.id == job_id) \
                .update({'status': status})

        self.session.commit()

    def add_products(self):
        pass

    def get_unsubscribe_link(self):
        pass


if __name__ == "__main__":
    pass
