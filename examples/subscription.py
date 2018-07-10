import json

import asf_hyp3


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


def sub_exists(api):
    sub_names = [
        sub['name'] for sub in get_subs(api)
    ]

    return get_sub_name() in sub_names


def get_subs(api):
    return api.get_subscriptions()


def get_sub_name():
    return 'Notify Only Example'


def make_sub(api):
    process_id = [
        p['id'] for p in api.get_processes() if 'Notify Only' in p['name']
    ].pop()

    resp = api.create_subscription(
        name=get_sub_name(),
        crop_to_selection=False,
        location=(
            'MULTIPOLYGON (((56.89 48.61,80.10 48.96,'
            '94.51 31.85,62.52 33.48,56.89 48.61)))'
        ),
        process_id=process_id,
        platform='Sentinel-1'
    )
    print(resp['status'])


if __name__ == "__main__":
    main()
