import json

import hyp3_db
from hyp3_db import hyp3_models

import send_email_queries as queries
import render
import ses
import sns


def send_email_main(aws_event):
    print('send email start')
    print(json.dumps(aws_event))

    print("getting start event")
    finish_event = sns.get_hyp3_event_from(aws_event)

    with hyp3_db.connect_using_environment_variables() as db:
        user = queries.get_user_by_email(db, finish_event.address)

        if not user:
            print('no known users can be identified from the requested email address, aborting...')
            return
        if not user.wants_email:
            print('user does not want emails, aborting...')
            return

        unsub_action = get_unsub_action(db, user.id)

    send_email_notification(finish_event, unsub_action)


def get_unsub_action(db, user_id):
    unsub_action = queries.get_unsub_action(db, user_id)

    if not unsub_action:
        unsub_action = hyp3_models.OneTimeAction.new_unsub_action(user_id)
        db.session.add(unsub_action)

    return unsub_action


def send_email_notification(finish_event, unsub_action):
    print("rendering email")
    subject, address = finish_event.subject, finish_event.address
    context = finish_event.to_dict()

    context['unsubscribe_url'] = unsub_action.url(
        # TODO: Put correct API url here
        api_url='www.api.example.com'
    )

    message = render.email_with(context)

    print('sending email')
    ses.send(
        address,
        subject,
        message
    )
