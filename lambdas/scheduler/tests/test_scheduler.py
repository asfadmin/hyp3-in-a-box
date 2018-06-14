import import_scheduler
import schedule
import testing_utils as utils
from db_cred_setup import skip_if_creds_not_availbable
from environment import environment


@skip_if_creds_not_availbable
def test_scheduler():
    granules = utils.load_testing_granules()

    email_packages = schedule.hyp3_jobs(granules)

    assert isinstance(email_packages, list)

    for sub, user, granule_package in email_packages:
        assert hasattr(sub, 'id')
        assert all(
            k in granule_package for k in ['name', 'download_url', 'polygon']
        )
        assert sub.user_id == user.id

    if 'local' in environment.maturity:
        utils.cache_results(email_packages)
