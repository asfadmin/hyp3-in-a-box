# setup_db.py
# Rohan Weeden, William Horn
# June 14, 2018

# Database setup functions. Need to pull them out from lambda_function to avoid
# naming conflicts during unit test imports

import collections
import json

import sqlalchemy
from sqlalchemy import sql

import hyp3_db
from hyp3_db.hyp3_models.base import Base
import custom_resource

import setup_db_utils as utils
import hyp3_user
import hyp3_processes
import ssm


def setup_db(event, db_admin_creds, db_user_creds):
    print(json.dumps(event))

    resp = DBSetup(event, db_admin_creds, db_user_creds) \
        .get_response()

    custom_resource.send(event, resp)


class DBSetup(custom_resource.Base):
    def __init__(self, event, db_admin_creds, db_user_creds):
        super().__init__(event)
        self.db_creds = db_admin_creds
        self.db_user_creds = db_user_creds

    def _process(self):
        print('connecting to hyp3_db')
        setup_outputs = {}
        with hyp3_db.connect(*self.db_creds, commit_on_close=True) as db:
            print('connected as root user')
            setup_outputs.update(
                setup_db_priviliged(db)
            )

        with hyp3_db.connect(*self.db_user_creds, commit_on_close=True) as db:
            print('connected as hyp3 user')
            setup_outputs.update(
                setup_db_low_privileged(db)
            )

        assert 'HyP3ApiKey' in setup_outputs
        assert 'HyP3Username' in setup_outputs

        return {
            'Data': setup_outputs,
            'Reason': 'Successfully setup hyp3 db'
        }


def setup_db_priviliged(db):
    """ Creates hyp3 user and postgis extension """

    print('Setting up database:')
    steps = [
        install_postgis,
        add_db_user
    ]

    return setup_db_steps(db, steps)


def setup_db_low_privileged(db):
    """ Creates all database tables """

    print('Creating/populating tables:')
    steps = [
        make_tables,
        make_hyp3_admin_user,
        add_default_processes
    ]

    return setup_db_steps(db, steps)


def setup_db_steps(db, steps):
    output = {}
    for i, step in enumerate(steps):
        count, num_steps = i + 1, len(steps)

        print(f'{count}/{num_steps} - {step.__name__}')

        step_output = step(db)

        if not step_output:
            continue

        output.update(step_output)

    db.session.commit()

    return output


def install_postgis(db):
    create_postgis_sql = sql.text("""
        CREATE EXTENSION postgis;
    """)

    try:
        db.engine.execute(create_postgis_sql)
    except sqlalchemy.exc.ProgrammingError:
        print('postgis already installed')


def add_db_user(db):
    user, password, db_name = utils.get_environ_params(
        'HyP3DBUser',
        'HyP3DBPass',
        'HyP3DBName'
    )

    if does_db_user_exists(db, user):
        print(f'user {user} already exists')
        return

    add_user_sql = sql.text(f"""
        CREATE USER {user} WITH PASSWORD :password;
        GRANT ALL PRIVILEGES ON DATABASE {db_name} to {user};
    """)

    db.engine.execute(
        add_user_sql,
        password=password
    )


def does_db_user_exists(db, user):
    check_user_sql = sql.text("""
        SELECT 1 FROM pg_roles WHERE rolname=:user;
    """)

    return db.engine.execute(
        check_user_sql,
        user=user
    ).fetchone()


def make_tables(db):
    Base.metadata.create_all(db.engine)


User = collections.namedtuple('User', ['name', 'email'])


def make_hyp3_admin_user(db):
    user = get_user()
    param_paths = get_param_store_paths()

    if hyp3_user.is_new(db, user):
        print('Creating new user')
        step_output = add_new_user(db, user, param_paths)
    else:
        print('User already exists')
        step_output = reference_old_user_params(param_paths)

    return step_output


def get_param_store_paths():
    stack_name = utils.get_environ_params('HyP3StackName').pop()
    [username_param_name, api_key_param_name] = utils.get_environ_params(
        "ParamNameHyP3Username",
        "ParamNameHyP3ApiKey"
    )
    print(stack_name)

    return {
        'username': '/{}/{}'.format(stack_name, username_param_name),
        'api-key': '/{}/{}'.format(stack_name, api_key_param_name)
    }


def get_user():
    name, email = utils.get_environ_params(
        'HyP3AdminUsername',
        'HyP3AdminEmail'
    )

    return User(name, email)


def add_new_user(db, user, param_paths):
    api_key = hyp3_user.add_to(db, user)

    ssm.save_params({
        param_paths['api-key']: api_key,
        param_paths['username']: user.name
    })

    return {
        'HyP3ApiKey': api_key,
        'HyP3Username': user.name
    }


def reference_old_user_params(param_paths):
    print('hyp3 user already exists')

    prefix = 'SSM Parameter Store Path -> '

    return {
        'HyP3ApiKey': prefix + param_paths['api-key'],
        'HyP3Username': prefix + param_paths['username']
    }


def add_default_processes(db):
    new_processes = hyp3_processes.new(db)

    db.session.bulk_save_objects(new_processes)
