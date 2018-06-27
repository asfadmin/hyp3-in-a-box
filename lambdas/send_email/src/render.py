from render_email import Email


def email_with(event):
    context = event.to_dict()

    return Email('email.html.j2') \
        .render(**context)
