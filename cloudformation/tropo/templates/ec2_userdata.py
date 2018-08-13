from textwrap import dedent

from tropo_env import environment
from troposphere import Base64, Ref, Sub


def make_userdata_from_environment():
    return dedent("""
        #! /bin/bash
        echo STACK_NAME=${{StackName}} > ~/env

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
        sudo apt-get update
        sudo apt-get install -y awscli

        CLONE_TOKEN=$(aws ssm get-parameters --names /CodeBuild/GITHUB_HYP3_API_CLONE_TOKEN --output text --with-decryption | awk {'print $4'})
        cd /tmp
        git clone --single-branch -b dev https://$CLONE_TOKEN@github.com/asfadmin/hyp3-in-a-box --depth=1

        pushd hyp3-in-a-box/processes/rtc_snap/.
            sudo python3.6 install.py
        popd

        pushd hyp3-in-a-box/ec2/worker/.
            sudo ./install.sh
        popd
        """).strip()


user_data = Base64(
    Sub(
        make_userdata_from_environment(),
        StackName=Ref('AWS::StackName')
    )
)
