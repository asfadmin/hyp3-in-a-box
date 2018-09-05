"""
Generates the UserData script for setting up the EC2 instances. In production
mode the userdata only needs to set the stack name environment variable and
start the HyP3 daemon service.
"""

from textwrap import dedent
import pathlib as pl

from tropo_env import environment
from troposphere import Base64, Ref, Sub


def make_userdata_from_environment():
    """ Generate userdata, and optionally insert the development mode install
    commands if ``--maturity`` is not ``prod`` or ``stage``.
    """

    update_code = get_hyp3_daemon_install_script() \
        if environment.maturity not in ["prod", "stage"] \
        else ""

    return dedent("""
        #! /bin/bash
        echo STACK_NAME=${{StackName}} > /home/ubuntu/env

        {UpdateCode}

        sudo systemctl restart hyp3
        """).strip().format(
        UpdateCode=update_code
    )


def get_hyp3_daemon_install_script():
    """ This only exists for the purpose of development. Instead of needing to
    create a new AMI when the orchestration code changes, just let the AMI pull
    the new version of the code on startup."""

    path = pl.Path(__file__).parent / './hyp3_daemon_install.sh'

    with path.open('r') as f:
        return f.read().strip()


user_data = Base64(Sub(
    make_userdata_from_environment(),
    StackName=Ref('AWS::StackName')
))
