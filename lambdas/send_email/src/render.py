from render_email import Email


def email_with(context):
    return Email('email.html.j2') \
        .render(**context)
