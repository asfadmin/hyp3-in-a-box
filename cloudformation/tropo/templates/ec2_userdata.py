"""
Generates the UserData script for setting up the EC2 instances. In production
mode the userdata only needs to set the stack name environment variable and
start the HyP3 daemon service.
"""

from textwrap import dedent

from tropo_env import environment
from troposphere import Base64, Ref, Sub


def make_userdata_from_environment():
    """ Generate userdata, and optionally insert the development mode install
    commands if ``--clone_in_userdata`` was set.
    """
    return dedent("""
        #! /bin/bash
        echo STACK_NAME=${{StackName}} > /home/ubuntu/env

        {PullCode}

        sudo systemctl restart hyp3
        """).strip().format(
        PullCode=get_hyp3_daemon_install_script() if environment.clone_in_userdata
        else ""
    )


def get_hyp3_daemon_install_script():
    """ This only exists for the purpose of development. Instead of needing to
    create a new AMI when the orchestration code changes, just let the AMI pull
    the new version of the code on startup."""

    return dedent("""
        CLONE_TOKEN=$(aws ssm get-parameter --name /CodeBuild/GITHUB_HYP3_API_CLONE_TOKEN --output text --with-decryption | awk {'print $6'})

        cd /home/ubuntu
        rm -rf ./hyp3-in-a-box

        git clone --single-branch -b dev https://$CLONE_TOKEN@github.com/asfadmin/hyp3-in-a-box --depth=1

        pushd hyp3-in-a-box/processes/rtc_snap/.
            sudo python3.6 install.py $CLONE_TOKEN
        popd

        pushd hyp3-in-a-box/ec2/worker/.
            sudo ./install.sh
        popd

        sudo systemctl daemon-reload
        echo "-Xmx32G" > /usr/local/snap/bin/gpt.vmoptions
        """).strip()


user_data = Base64(
    Sub(
        make_userdata_from_environment(),
        StackName=Ref('AWS::StackName')
    )
)
