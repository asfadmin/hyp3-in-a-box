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

import requests

GITHUB_API_ENDPOINT = "https://api.github.com"
GITHUB_STATUS_CONTEXT = "continuous-integration/codebuild"
GITHUB_REPOSITORY_NAME = "asfadmin/hyp3-in-a-box"
GITHUB_BRANCH = "dev"
S3_SOURCE_BUCKET = "hyp3-in-a-box-source"

MATURITY = os.environ["MATURITY"]
GITHUB_STATUS_TOKEN = os.environ["GITHUB_STATUS_TOKEN"]
GITHUB_COMMIT_HASH = os.environ["CODEBUILD_RESOLVED_SOURCE_VERSION"]


def install():
    update_github_status("pending", description="Build in progress")
    subprocess.call(["pip", "install", "-U", "-r", "build_requirements.txt"])
    subprocess.call(["pip", "install", "-U", "-r", "build_requirements.txt"])
    os.chmod("upload.sh", stat.S_IEXEC)


def pre_build():
    subprocess.call(["python3", "-m", "pytest"])


def build():
    os.makedirs("build/lambdas")
    subprocess.call(["python3", "cloudformation/tropo/create_stack.py", "build/template.json", "--maturity", MATURITY])
    subprocess.call(["python3", "lambdas/build_lambda.py", "-a", "-o", "build/lambdas/ lambdas/"])


def post_build():
    bucket_base_dir = os.path.join(S3_SOURCE_BUCKET, MATURITY + "/")
    subprocess.call(["aws", "s3", "cp", "s3://{}".format(os.path.join(bucket_base_dir, "config/configuration.json")), "build/"])
    subprocess.call(["aws", "s3", "cp", "build/lambdas/", "s3://{}".format(bucket_base_dir), "--recursive", "--include", '"*"'])
    update_github_status("success", description="Build completed")


def update_github_status(state, description=None):
    url = urljoin(GITHUB_API_ENDPOINT, "repos", GITHUB_REPOSITORY_NAME, "statuses", GITHUB_COMMIT_HASH)
    data = {
        "state": state,
        "context": GITHUB_STATUS_CONTEXT,
        "description": description
    }
    requests.get(url, params={"access_token": GITHUB_STATUS_TOKEN}, data=data)


def write_tmp_status(code):
    with open("/tmp/status", "w") as f:
        f.write(str(code))


def main(step=None):
    build_ok = True
    if os.path.exists("/tmp/status"):
        with open("/tmp/status", "r") as f:
            s = f.read()
            if s != "0":
                build_ok = False
    step_function_table = {
        "install": install,
        "pre_build": pre_build,
        "build": build,
        "post_build": post_build
    }

    try:
        if build_ok:
            return step_function_table.get(step, lambda: None)()
            write_tmp_status(0)
        else:
            return
    except subprocess.CalledProcessError as e:
        update_github_status("failure", description=step)
        write_tmp_status(e.returncode)
        raise
    except Exception:
        update_github_status("error")
        write_tmp_status(-1337)
        raise


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(step=sys.argv[1])
    else:
        main()
