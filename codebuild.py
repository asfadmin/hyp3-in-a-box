# codebuild.py
# Rohan Weeden
# Created: June 8, 2018

# Called by buildspec.yml. This script improves the codebuild functionality
# From the defaults.
# - Keep track of overall build status
# - Stop doing build actions when a step fails
# - Update GitHub status appropriately

import os
import stat
import subprocess
import sys
from urllib.parse import urljoin
from xml.etree import ElementTree

import requests

GITHUB_API_ENDPOINT = "https://api.github.com"
GITHUB_STATUS_CONTEXT = "continuous-integration/codebuild"
GITHUB_REPOSITORY_NAME = "asfadmin/hyp3-in-a-box"
GITHUB_BRANCH = "dev"
S3_SOURCE_BUCKET = "hyp3-in-a-box-source"
S3_STATUS_BUCKET = "asf-docs/hyp3-in-a-box"

MATURITY = os.environ["MATURITY"]
GITHUB_STATUS_TOKEN = os.environ["GITHUB_STATUS_TOKEN"]
GITHUB_COMMIT_HASH = os.environ["CODEBUILD_RESOLVED_SOURCE_VERSION"]

BUCKET_BASE_DIR = os.path.join(S3_SOURCE_BUCKET, MATURITY + "/")

build_step_failure_message = None
test_result_summary = ""


def install():
    update_github_status("pending", description="Build in progress")
    install_all_requirements_txts(".")
    os.chmod("upload.sh", stat.S_IEXEC)


def pre_build():
    global test_result_summary
    global build_step_failure_message

    try:
        subprocess.check_call(["python3", "-m", "pytest", "--junitxml=/tmp/test_results.xml"])
    except subprocess.CalledProcessError as e:
        raise e
    finally:
        r = ElementTree.parse("/tmp/test_results.xml").getroot()
        test_result_summary = "{} Tests, {} Failed, {} Errors".format(
            r.get("tests"),
            r.get("failed"),
            r.get("errors")
        )
        build_step_failure_message = test_result_summary


def build():
    os.makedirs("build/lambdas")
    subprocess.check_call(["python3", "cloudformation/tropo/create_stack.py", "build/template.json", "--maturity", MATURITY])
    subprocess.check_call(["python3", "lambdas/build_lambda.py", "-a", "-o", "build/lambdas/", "lambdas/"])
    subprocess.check_call(["./upload.sh", "docs"])


def post_build():
    subprocess.check_call(["aws", "s3", "cp", "s3://{}".format(os.path.join(BUCKET_BASE_DIR, "config/configuration.json")), "build/"])
    subprocess.check_call(["aws", "s3", "cp", "build/lambdas/", "s3://{}".format(BUCKET_BASE_DIR), "--recursive", "--include", '"*"'])
    update_github_status("success", description="Build completed")


def install_all_requirements_txts(root_path):
    for (path, dirs, files) in os.walk(root_path):
        for name in files:
            if name == "requirements.txt":
                subprocess.check_call(["pip", "install", "-U", "-r", os.path.join(path, name)])


def set_github_ci_status(status, description=None):
    svg_status = "passing"
    if status != "success":
        svg_status = "failing"

    with open("build/status.svg", "w") as f:
        f.write(get_svg_status(svg_status))

    subprocess.check_call(["aws", "s3", "cp", "build/status.svg", "s3://{}".format(os.path.join(S3_STATUS_BUCKET, "build_status.svg"))])

    update_github_status(status, description=description)


def update_github_status(state, description=None):
    url = urljoin(GITHUB_API_ENDPOINT, "repos/{}/statuses/{}".format(GITHUB_REPOSITORY_NAME, GITHUB_COMMIT_HASH))
    data = {
        "state": state,
        "context": GITHUB_STATUS_CONTEXT,
        "description": description
    }
    requests.post(url, params={"access_token": GITHUB_STATUS_TOKEN}, json=data)


def save_status(code):
    os.environ["BUILD_STATUS"] = str(code)


def get_status():
    return os.environ.get("BUILD_STATUS", "0")


def main(step=None):
    step_function_table = {
        "install": install,
        "pre_build": pre_build,
        "build": build,
        "post_build": post_build
    }

    try:
        if get_status() == "0":
            return step_function_table.get(step, lambda: None)()
            save_status(0)
        else:
            return
    except subprocess.CalledProcessError as e:
        desc = step
        global build_step_failure_message
        if build_step_failure_message is not None:
            desc = build_step_failure_message
        update_github_status("failure", description=desc)
        save_status(e.returncode)
        raise
    except Exception:
        update_github_status("error")
        save_status(-1337)
        raise


def get_svg_status(status):
    color = "#4c1"
    if status == "failing":
        color = "#e05d44"
    svg = """<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" width="90" height="20">
  <linearGradient id="a" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <rect rx="3" width="90" height="20" fill="#555"/>
  <rect rx="3" x="37" width="53" height="20" fill="{color}"/>
  <path fill="{color}" d="M37 0h4v20h-4z"/>
  <rect rx="3" width="90" height="20" fill="url(#a)"/>
  <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
    <text x="19.5" y="15" fill="#010101" fill-opacity=".3">build</text>
    <text x="19.5" y="14">build</text>
    <text x="62.5" y="15" fill="#010101" fill-opacity=".3">{status}</text>
    <text x="62.5" y="14">{status}</text>
  </g>
</svg>
""".format(status=status, color=color)
    return svg


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(step=sys.argv[1])
    else:
        main()
