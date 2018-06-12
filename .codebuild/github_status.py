# github_status.py
# Rohan Weeden
# Created: June 11, 2018

# Functions for setting github status

import os
import subprocess
from urllib.parse import urljoin

import requests

GITHUB_API_ENDPOINT = "https://api.github.com"
GITHUB_STATUS_CONTEXT = "continuous-integration/codebuild"
GITHUB_REPOSITORY_NAME = "asfadmin/hyp3-in-a-box"
S3_STATUS_BUCKET = "asf-docs/hyp3-in-a-box"

MATURITY = os.environ["MATURITY"]
GITHUB_STATUS_TOKEN = os.environ.get("GITHUB_STATUS_TOKEN", "")
GITHUB_COMMIT_HASH = os.environ["CODEBUILD_RESOLVED_SOURCE_VERSION"]

print(os.environ)


def set_github_ci_status(status, description=None):
    svg_status = "passing"
    if status != "success":
        svg_status = "failing"

    with open("build/status.svg", "w") as f:
        f.write(get_svg_status(svg_status))

    subprocess.check_call(["aws", "s3", "cp", "build/status.svg", "s3://{}".format(os.path.join(S3_STATUS_BUCKET, MATURITY + "-build-status.svg")), "--acl", "public-read", "--cache-control", "no-cache"])

    update_github_status(status, description=description)


def update_github_status(state, description=None):
    url = urljoin(GITHUB_API_ENDPOINT, "repos/{}/statuses/{}".format(GITHUB_REPOSITORY_NAME, GITHUB_COMMIT_HASH))
    data = {
        "state": state,
        "context": GITHUB_STATUS_CONTEXT,
        "description": description
    }
    requests.post(url, params={"access_token": GITHUB_STATUS_TOKEN}, json=data)


def get_svg_status(status):
    color = "brightgreen"
    if status == "failing":
        color = "red"

    url = 'https://img.shields.io/badge/build-{status}-{color}.svg'.format(
        status=status, color=color
    )
    r = requests.get(url)

    return r.text
