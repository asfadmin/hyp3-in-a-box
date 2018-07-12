import json

import sns
import render
import ses


def send_email_main(aws_event):
    print(json.dumps(aws_event))

    print("getting start event")
    finish_event = sns.get_hyp3_event_from(aws_event)

    print("rendering email")
    subject, address = finish_event.subject, finish_event.address
    message = render.email_with(finish_event)

    if not finish_event.browse_url:
        print("no browse_url so not sending email...")
        return

    print('sending email')
    ses.send(
        address,
        subject,
        message
    )
