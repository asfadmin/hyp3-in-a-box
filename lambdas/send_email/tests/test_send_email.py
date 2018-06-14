import import_send_email
from render_email import Email

example_params = {
    'download_url': 'www.hello.html',
    'subject': 'New Data For Subscription',
    'browse_url': 'https://hyp3-download.asf.alaska.edu/hyp3/browse/dis_mag+S1_20180504T033546_S1_20180528T033547+256-64_50-10_0.00-0.08_2_geo.png',
    'unsubscribe_url': 'https://unsubscribe.example.com',
    'additional_info': [
        {'name': 'granule name', 'value': '777778'}
    ]
}


def test_email_class():
    email_obj = Email('email.html.j2')
    rendered_output = email_obj.render(**example_params)

    assert isinstance(rendered_output, str)
    assert example_params['additional_info'][0]['name'] in rendered_output
    assert example_params['additional_info'][0]['value'] in rendered_output
    for item in example_params.items():
        if isinstance(item, str):
            assert item in rendered_output
