import json
import pathlib as pl


def cache_results(email_packages):
    packages = [
        (serializeable(sub), serializeable(user), gran) for
        sub, user, gran in email_packages
    ]

    with (pl.Path(__file__).parent / 'data' / 'email-packages.json').open('w') as f:
        json.dump(packages, f, indent=2)


def serializeable(sub):
    sub_dict = {}
    for k, v in sub.__dict__.items():
        try:
            json.dumps(v)
        except TypeError:
            continue

        sub_dict[k] = v

    return sub_dict
