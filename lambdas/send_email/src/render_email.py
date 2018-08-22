# render_email.py
# William Horn
# Created: June 2018

import abc
import pathlib as pl
import jinja2 as j2


class Email(abc.ABC):
    ''' Email object for generating an HTML email from Jinja2 template'''

    def __init__(self, template_name='email.html.j2'):
        self.template_name = template_name

    def render(self, **kwargs):
        ''' Generate the email HTML using the given context.

            :param kwargs: The Jinja2 template context

                * subject - Email subject
                * additional_info - list[dict] containing meta data about event
                    * name - Metadata title
                    * value - Metadata content
                * browse_url - URL of a browse image to display
                * download_url - URL where the processed data can be downloaded
                * unsubscribe_url - URL to disable email notifications

            :returns: The rendered message
            :rtype: string
        '''
        env = get_env()

        temp = env.get_template(self.template_name)

        return temp.render(kwargs)


def get_env():
    ''' Get the Jinja2 environment for rendering emails

        :returns: The Jinja2 Environment
        :rtype: `jinja2.Environment <http://jinja.pocoo.org/docs/latest/api/#jinja2.Environment>`_
    '''
    env = j2.Environment(
        loader=get_loader(),
        autoescape=True
    )

    return env


def get_loader():
    templates_path = pl.Path(__file__).parent / 'templates'

    return j2.FileSystemLoader(str(templates_path))
