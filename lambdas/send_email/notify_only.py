
import jinja2 as j2
import abc


class Email(abc.ABC):
    def __init__(self, template_name):
        self.template_name = template_name

    def render(self, **kwargs):
        env = self.get_env()

        temp = env.get_template(self.template_name)

        return temp.render(kwargs)

    def get_env(self):
        env = j2.Environment(
            loader=j2.FileSystemLoader('templates'),
            autoescape=j2.select_autoescape(['html', 'xml'])
        )

        return env


