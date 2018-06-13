# render_email.py
# William Horn
# Created: June 2018

import jinja2 as j2
import abc
import os


class Email(abc.ABC):
    ''' Email object for generating an HTML email from Jinja2 template'''
    def __init__(self, template_name):
        self.template_name = template_name

    def render(self, **kwargs):
        ''' Generate the email HTML using the given context.

            :param \*\*kwargs: The Jinja2 template context

                * subject - Email subject
                * additional_info - A list of dictionaries containing more meta data about the processing event
                    * name - Metadata title
                    * value - Metadata content
                * browse_url - URL of a browse image to display
                * download_url - URL where the processed data can be downloaded from
                * unsubscribe_url - URL to disable email notifications of this type

            :returns: The rendered message
            :rtype: string
        '''
        env = self.get_env()

        temp = env.get_template(self.template_name)

        return temp.render(kwargs)

    def get_env(self):
        ''' Get the Jinja2 environment for rendering emails

            :returns: The Jinja2 Environment
            :rtype: `jinja2.Environment <http://jinja.pocoo.org/docs/latest/api/#jinja2.Environment>`_
        '''
        env = j2.Environment(
            loader=j2.FileSystemLoader(
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    'templates'
                )
            ),
            autoescape=j2.select_autoescape(['html', 'xml'])
        )

        return env
