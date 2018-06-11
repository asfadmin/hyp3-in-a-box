
import import_path
from hyp3_db import Hyp3DB


def test_get_enabled_subs():
    db = Hyp3DB()
    enabled_subs = db.get_enabled_subs()

    for sub in enabled_subs:
        assert sub.enabled is True
