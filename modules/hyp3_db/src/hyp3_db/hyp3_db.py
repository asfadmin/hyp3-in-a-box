from geoalchemy2 import WKTElement
from sqlalchemy import sql

from .hyp3_models import LocalQueue, Subscription, User
from .session import make_engine, make_session


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
        self.engine = make_engine(
            user=user,
            password=password,
            host=host
        )
        self.session = make_session(self.engine)

    def get_users_by_ids(self, user_ids):
        user_ids_filter = User.id.in_(user_ids)

        users = self.session.query(User) \
            .filter(user_ids_filter) \
            .all()

        return users

    def get_enabled_subs(self):
        subs = self.enabled_subs_query.all()

        return subs

    def get_enabled_intersecting_subs(self, polygon):
        poly = WKTElement(polygon, srid=4326)
        intersection = Subscription.location.ST_Contains(poly)

        intersecting_subs = self.enabled_subs_query \
            .filter(intersection) \
            .all()

        return intersecting_subs

    @property
    def enabled_subs_query(self):
        return self.session.query(Subscription) \
            .filter_by(enabled=True)

    def get_job(self, job_id):
        return self.session                  \
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
            raise ValueError('{} not a valid job_status.'.format(status))

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
