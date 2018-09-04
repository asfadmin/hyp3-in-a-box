import json
from typing import Dict

import hyp3_db
from hyp3_db import hyp3_models
from hyp3_db.hyp3_models import OneTimeAction, User
from hyp3_events import EmailEvent

from render_email import Email
import send_email_queries as queries
import ses
import send_email_sns as sns
from send_email_env import environment


def send_email_main(aws_event: Dict) -> None:
    print('send email start')
    print(json.dumps(aws_event))

    print("getting start event")
    email_event = sns.get_hyp3_event_from(aws_event)
    if not isinstance(email_event, EmailEvent):
        raise Exception("Read wrong type of event!")

    with hyp3_db.connect_using_environment_variables(commit_on_close=True) as db:
        user = queries.get_user_by_id(db, email_event.user_id)

        if not user.wants_email:
            print('user does not want emails, aborting...')
            return

        unsub_action = get_action(db, user.id, action_type='unsubscribe')
        disable_sub_action = get_action(
            db,
            user.id,
            action_type='disable_subscription',
            params=str(email_event.sub_id)
        )

        context = make_email_context(
            db, user, unsub_action, disable_sub_action, email_event
        )

        send_email_notification(user, context)


def get_action(db, user_id, action_type, params=None) -> OneTimeAction:
    action = queries.get_action(db, user_id, action_type, params)

    if not action:
        new_action = hyp3_models.OneTimeAction.new_action(
            user_id,
            action_type,
            params
        )

        db.session.add(new_action)
        action = update_obj(db, new_action)

    return action


def update_obj(db, obj):
    db.session.flush()
    db.session.refresh(obj)

    return obj


def make_email_context(
    db: hyp3_db.HyP3DB,
    user: User,
    unsub_action: OneTimeAction,
    disable_sub_action: OneTimeAction,
    email_event: EmailEvent
) -> Dict:
    sub = queries.get_sub_by_id(db, email_event.sub_id)

    context = {
        'unsubscribe_url': unsub_action.url(
            api_url=environment.api_url
        ),
        'disable_sub_url': disable_sub_action.url(
            api_url=environment.api_url
        ),
        'additional_info': email_event.additional_info + [{
            'name': 'User',
            'value': user.username
        }, {
            'name': 'Process',
            'value': sub.process.name,
        }, {
            'name': 'Subscripton',
            'value': sub.name
        }, {
            'name': 'Granule',
            'value': email_event.granule_name
        }],
        'download_url': email_event.download_url,
        'browse_url': email_event.browse_url,
        'api_url': environment.api_url
    }

    return context


def send_email_notification(user: User, context) -> None:
    print("rendering email")

    status = get_additional_info_field(context, "Status", default="")
    sub_name = get_additional_info_field(context, "Subscripton")
    process_name = get_additional_info_field(context, "Process")

    subject = f"{status} {sub_name} new {process_name} data"

    message = Email().render(**context)

    print('sending email')
    ses.send(
        user.email,
        subject,
        message
    )


def get_additional_info_field(context, key, default=None):
    for entry in context['additional_info']:
        if entry['name'] == key:
            return entry['value']

    return default
