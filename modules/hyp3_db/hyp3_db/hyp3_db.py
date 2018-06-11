
from .session import session
from .hyp3_models import Subscription, LocalQueue


class Hyp3DB:
    def __init__(self):
        pass

    def get_enabled_subs(self):
        subs = session                            \
            .query(Subscription)                  \
            .filter(Subscription.enabled is True) \
            .all()

        return subs

    def get_job(self, job_id):
        return session \
            .query(LocalQueue).limit(5).all()

    def add_job(self, job):
        pass

    def update_job(self, job):
        pass

    def add_products(self):
        pass

    def get_unsubscribe_link(self):
        pass


if __name__ == "__main__":
    pass
