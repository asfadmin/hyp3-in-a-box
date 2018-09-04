import import_hyp3_db
from hyp3_db import hyp3_models


def test_new_unsub_action():
    unsub_action = hyp3_models.OneTimeAction.new_action(1, 'unsubscribe')

    assert unsub_action
    assert unsub_action.user_id == 1
