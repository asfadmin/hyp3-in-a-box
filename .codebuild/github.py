# github_status.py
# Rohan Weeden
# Created: June 11, 2018

# Functions for setting github status

import os
import subprocess
from urllib.parse import urljoin

import requests

GITHUB_API_ENDPOINT = "https://api.github.com"
GITHUB_STATUS_CONTEXT = "CodeBuild Unit Tests"
GITHUB_REPOSITORY_NAME = "asfadmin/hyp3-in-a-box"
S3_STATUS_BUCKET = "asf-docs/hyp3-in-a-box"

MATURITY = os.environ["MATURITY"]
GITHUB_STATUS_TOKEN = os.environ.get("GITHUB_STATUS_TOKEN", "")
GITHUB_COMMIT_HASH = os.environ["CODEBUILD_RESOLVED_SOURCE_VERSION"]


def set_github_ci_status(status, description=None):
    svg_status = "passing" if status == "success" else "failing"

    color = "brightgreen"
    if svg_status == "failing":
        color = "red"

    write_status_to_s3("build", svg_status, color)
    update_github_status(status, description=description)


def write_status_to_s3(subject, status, color):
    if not os.path.exists(subject):
        os.makedirs(subject)

    svg_path = os.path.join(subject, "status.svg")
    with open(svg_path, "w") as f:
        f.write(get_svg_status(subject, status, color))

    s3_object_name = "s3://{}".format(
        os.path.join(S3_STATUS_BUCKET, MATURITY + "-{}-status.svg".format(subject))
    )

    subprocess.check_call([
        "aws", "s3", "cp", svg_path,
        s3_object_name, "--acl", "public-read",
        "--cache-control", "no-cache"
    ])


def update_github_status(state, description=None):
    url = urljoin(
        GITHUB_API_ENDPOINT,
        "repos/{}/statuses/{}".format(GITHUB_REPOSITORY_NAME,
                                      GITHUB_COMMIT_HASH)
    )
    data = {
        "state": state,
        "context": GITHUB_STATUS_CONTEXT,
        "description": description
    }
    requests.post(url, params={"access_token": GITHUB_STATUS_TOKEN}, json=data)


def get_svg_status(subject, status, color):
    url = 'https://img.shields.io/badge/{subject}-{status}-{color}.svg'.format(
        subject=subject, status=status, color=color
    )
    r = requests.get(url)

    return r.text


def create_release(version):
    url = urljoin(
        GITHUB_API_ENDPOINT,
        "repos/{}/releases".format(GITHUB_REPOSITORY_NAME)
    )
    requests.post(url, params={"access_token": GITHUB_STATUS_TOKEN}, data={
        "tag_name": version,
        "target_commitish": "master",
        "name": version
    })
