import jinja2 as j2
import pathlib as pl


def render():
    params = {
        'download_url': 'www.hello.html',
        'subject': 'New Data For Subscription',
        'browse_url': 'https://hyp3-download.asf.alaska.edu/hyp3/browse/dis_mag+S1_20180504T033546_S1_20180528T033547+256-64_50-10_0.00-0.08_2_geo.png',
        'additional_info': [
            {'name': 'granule name', 'value': '777778'}
        ]

    }

    email = render_template('email.html.j2', **params)

    with open('output.html', 'w') as f:
        f.write(email)


def render_template(template_name, **kwargs):
    env = get_env()

    temp = env.get_template(template_name)

    return temp.render(kwargs)


def get_env():
    path = pl.Path(__file__).parent
    print(path.absolute())

    env = j2.Environment(
        loader=j2.FileSystemLoader('templates'),
        autoescape=j2.select_autoescape(['html', 'xml'])
    )

    return env


if __name__ == "__main__":
    render()
