
import sns
import render
import ses


def send_email_main(aws_event):
    finish_event = sns.get_hyp3_event_from(aws_event)

    subject, address = finish_event.subject, finish_event.address
    message = render.email_with(finish_event)

    if finish_event.browse_url == "":
        return

    ses.send(
        address,
        subject,
        message
    )
