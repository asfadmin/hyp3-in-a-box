
import import_hyp3_db
from hyp3_db import hyp3_models


def test_new_unsub_action():
    print(dir(hyp3_models))
    unsub_action = hyp3_models.OneTimeAction.new_unsub_action(1)

    assert unsub_action
