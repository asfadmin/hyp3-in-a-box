import argparse
import collections
import textwrap
import json
import pathlib as pl

import asf_hyp3
import cache


Subscription = collections.namedtuple(
    'Subscription', ['name', 'location', 'process_name']
)


class CustomFormatter(
        argparse.ArgumentDefaultsHelpFormatter,
        argparse.RawDescriptionHelpFormatter
):
    """ Custom formatter for the argument parser"""


def main():
    parser = get_parser()
    args = vars(parser.parse_args())

    make(**args)


def get_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""\
            Create a list of subscriptions from a  json file
            each sub in the file will have the shape:

            {
                "name": <String name>,
                "location": "MULTIPOLYGON(((<multipolygon here>)))",
                "process_name": <valid hyp3 process name>
            }

            Subscription with the same name will not be recreated.
        """)
    )

    parser.add_argument(
        '--subs-file-path',
        required=True,
        help="path to the subscription json file"
    )

    return parser


def make(*, subs_file_path):
    api = get_api()

    subs = list(set(
        Subscription(**sub) for sub in get_new_subs_from(subs_file_path)
    ))

    return [
        make_sub(api, sub) for sub in subs if not sub_exists(api, sub.name)
    ]


def get_api():
    with (pl.Path(__file__).parent / 'cfg' / 'cfg.json').open('r') as f:
        cfg = json.load(f)

    return asf_hyp3.API(**cfg)


def sub_exists(api, sub_name):
    sub_names = [
        sub['name'] for sub in get_subs(api)
    ]

    return sub_name in sub_names


def get_new_subs_from(subs_file_path):
    with pl.Path(subs_file_path).open('r') as f:
        return json.load(f)


def make_sub(api, sub):
    process_id = [
        p['id'] for p in get_processes(api) if sub.process_name in p['name']
    ].pop()

    print(sub.location)

    params = {
        "name": sub.name,
        "location": sub.location,
        "process_id": process_id,
        "crop_to_selection": False,
        "process_id": process_id,
        "platform": 'Sentinel-1',
        "process_id": process_id
    }

    resp = api.create_subscription(**params)
    print(resp['status'])


@cache.with_name('subscriptions')
def get_subs(api):
    return api.get_subscriptions()


@cache.with_name('processes')
def get_processes(api):
    return api.get_processes()


if __name__ == "__main__":
    main()
