import json

import hyp3_db
import render
import send_email_queries as queries
import ses
import sns
from hyp3_db import hyp3_models
from send_email_env import environment


def send_email_main(aws_event):
    print('send email start')
    print(json.dumps(aws_event))

    print("getting start event")
    sns_message = sns.get_message_from(aws_event)

    with hyp3_db.connect_using_environment_variables(commit_on_close=True) as db:
        user = queries.get_user_by_id(db, sns_message['user_id'])

        if not user:
            print('Invalid user id, aborting...')
            return
        if not user.wants_email:
            print('user does not want emails, aborting...')
            return

        unsub_action = get_unsub_action(db, user.id)

        context = make_email_context(db, user, unsub_action, sns_message)
        send_email_notification(user, context)


def get_unsub_action(db, user_id):
    unsub_action = queries.get_unsub_action(db, user_id)

    if not unsub_action:
        unsub_action = hyp3_models.OneTimeAction.new_unsub_action(user_id)
        db.session.add(unsub_action)
        db.session.flush()
        db.session.refresh(unsub_action)

    return unsub_action


def send_email_notification(user, context, unsub_action):
    print("rendering email")
    subject, address = "[HyP3] New data available", user.email

    message = render.email_with(context)

    print('sending email')
    ses.send(
        address,
        subject,
        message
    )


def make_email_context(db, user, unsub_action, sns_message):
    sub = queries.get_sub_by_id(db, sns_message['sub_id'])
    context = {}
    context['unsubscribe_url'] = unsub_action.url(
        api_url=environment.api_url
    )
    context['additional_info'] = [{
        'name': 'User',
        'value': user.username
    }, {
        'name': 'Subscripton',
        'value': sub.name
    }, {
        'name': 'Granule',
        'value': sns_message['granule_name']
    }]
    pass
