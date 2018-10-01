"""
Generates the UserData script for setting up the EC2 instances. In production
mode the userdata only needs to set the stack name environment variable and
start the HyP3 daemon service.
"""

from textwrap import dedent
import pathlib as pl

from troposphere import Base64, Ref, Sub

from tropo_env import environment


def make_userdata_from_environment(process_name):
    """ Generate userdata, and optionally insert the development mode install
    commands if ``--maturity`` is not ``prod`` or ``stage``.
    """
    return dedent(
        """
        #! /bin/bash

        cd /home/ubuntu
        PROCESS={Process}

        {UpdateCode}

        cd hyp3-in-a-box/processes/$PROCESS/build/.

        python3.6 -m pipenv run \
            python -m hyp3_process --stack-name ${{StackName}}
        """
    ).strip().format(
        Process=process_name,
        UpdateCode=update_code()
    )


def update_code():
    """ This only exists for the purpose of development. Instead of needing to
    create a new AMI when the orchestration code changes, just let the AMI pull
    the new version of the code on startup."""

    if environment.maturity in ["prod", "stage"]:
        return ""
    else:
        return dedent("""
            CLONE_TOKEN=$(aws ssm get-parameter \
                --name /CodeBuild/GITHUB_HYP3_API_CLONE_TOKEN \
                --output text  \
                --with-decryption | awk {'print $4'})

            rm -rf ./hyp3-in-a-box

            git clone \
                --single-branch \
                -b dev \
                https://$CLONE_TOKEN@github.com/asfadmin/hyp3-in-a-box \
                --depth=1

            pushd hyp3-in-a-box/processes/$PROCESS/.
                pipenv install
                python3.6 install.py $CLONE_TOKEN
            popd
        """)


def user_data_for(process_name):
    return Base64(Sub(
        make_userdata_from_environment(process_name),
        StackName=Ref('AWS::StackName')
    ))
