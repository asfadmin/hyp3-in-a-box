import json
import os
from hashlib import sha1

import hyp3_db
import render
import ses
import sns

from hyp3_db.hyp3_models import OneTimeAction, User


def send_email_main(aws_event):
    print(json.dumps(aws_event))

    print("getting start event")
    finish_event = sns.get_hyp3_event_from(aws_event)

    with hyp3_db.connect_from_env() as db:
        user = db.session.query(User).filter_by(email=finish_event.address).first()
        if not user.wants_email:
            print('user does not want emails, aborting...')
            return

        unsub_action = db.session.query(OneTimeAction) \
            .filter_by(user_id=user.id) \
            .filter_by(action='unsubscribe') \
            .first()
        if not unsub_action:
            unsub_action = create_unsubscribe_action(user)
            db.session.add(unsub_action)
            db.session.commit()

        print("rendering email")
        subject, address = finish_event.subject, finish_event.address
        context = finish_event.to_dict()
        context['unsubscribe_url'] = create_unsubscribe_url(unsub_action)
        message = render.email_with(finish_event)

        print('sending email')
        ses.send(
            address,
            subject,
            message
        )


def create_unsubscribe_action(user):
    return OneTimeAction(
        user_id=user.id,
        action='unsubscribe',
        hash=sha1().update(os.urandom(128)).hexdigest()
    )


def create_unsubscribe_url(unsub_action):
    return "{}/onetime/unsubscribe?id={}&key={}".format(
        'https://api.example.com',
        unsub_action.id,
        unsub_action.hash
    )
