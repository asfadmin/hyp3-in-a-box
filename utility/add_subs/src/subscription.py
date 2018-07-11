import json

import asf_hyp3
import cache


def main():
    api = get_api()

    if not sub_exists(api):
        print('making new sub')
        make_sub(api)
    else:
        print('sub already exists')


def get_api():
    with open('cfg.json') as f:
        cfg = json.load(f)

    return asf_hyp3.API(**cfg)


def sub_exists(api, sub_name):
    sub_names = [
        sub['name'] for sub in get_subs(api)
    ]

    return sub_name in sub_names


def get_new_sub_params(api):
    return [{
        'name': 'Notify Only Example',
        'location': ('MULTIPOLYGON (((56.89 48.61,80.10 48.96,'
                     '94.51 31.85,62.52 33.48,56.89 48.61)))',
                     ),
        'process_name': 'Notify Only'
    }, {
        'name': 'Europe/Asia',
        'location': ('MULTIPOLYGON (((-22.04 78.05,164.98'
                     '78.05,164.98 6.97,-22.04 6.97,-22.04 78.05)))'),
        'process_name': 'Notify Only'
    }]


def make_sub(api, sub_params, process_name):
    process_id = [
        p['id'] for p in get_processes(api) if process_name in p['name']
    ].pop()

    params = {
        **sub_params,
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
