import notify_only as no


def render():
    params = {
        'download_url': 'www.hello.html',
        'subject': 'New Data For Subscription',
        'browse_url': 'https://hyp3-download.asf.alaska.edu/hyp3/browse/dis_mag+S1_20180504T033546_S1_20180528T033547+256-64_50-10_0.00-0.08_2_geo.png',
        'additional_info': [
            {'name': 'granule name', 'value': '777778'}
        ]

    }

    email = no.Email('email.html.j2') \
        .render(**params)

    with open('output.html', 'w') as f:
        f.write(email)


if __name__ == "__main__":
    render()
