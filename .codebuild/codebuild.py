# codebuild.py
# Rohan Weeden
# Created: June 8, 2018

# Called by buildspec.yml. This script improves the codebuild functionality
# From the defaults.
# - Keep track of overall build status
# - Stop doing build actions when a step fails
# - Update GitHub status appropriately

import json
import os
import stat
import subprocess
import sys
from xml.etree import ElementTree

import boto3
from github_status import set_github_ci_status, update_github_status

S3_SOURCE_BUCKET = "asf-hyp3-in-a-box-source"
MATURITY = os.environ["MATURITY"]
BUCKET_BASE_DIR = os.path.join(S3_SOURCE_BUCKET, MATURITY + "/")
BUILD_STEP_MESSAGES = {}


def install():
    update_github_status("pending", description="Build in progress")
    install_all_requirements_txts('.')
    os.chmod("upload.sh", stat.S_IEXEC)


def pre_build():
    try:
        subprocess.check_call(
            ["python3", "-m", "pytest", "--junitxml=/tmp/test_results.xml"])
    except subprocess.CalledProcessError as e:
        raise e
    finally:
        r = ElementTree.parse("/tmp/test_results.xml").getroot()
        test_result_summary = "{} Tests, {} Failed, {} Errors".format(
            int(r.get("tests", 0)) - int(r.get("skips", 0)),
            r.get("failures"),
            r.get("errors")
        )
        BUILD_STEP_MESSAGES['failure'] = test_result_summary
        save_config("TEST_RESULT_SUMMARY", test_result_summary)


def build():
    os.makedirs("build/lambdas")
    object_versions = build_lambdas()
    version_options = []
    for v in object_versions:
        version_options += ["--{}_version".format(v[0]), v[1]]

    subprocess.check_call([
        "python3", "cloudformation/tropo/create_stack.py",
        "build/template.json", "--maturity", MATURITY
    ] + version_options
    )
    subprocess.check_call(["make", "clean", "html"], cwd="docs")


def build_lambdas():
    subprocess.check_call([
        "python3", "lambdas/build_lambda.py", "-a",
        "-o", "build/lambdas/", "lambdas/"
    ])
    subprocess.check_call([
        "aws", "s3", "cp", "build/lambdas",
        "s3://{}".format(BUCKET_BASE_DIR),
        "--recursive",
        "--include", '"*"'
    ])
    print("Latest Source Versions:")
    versions = get_latest_lambda_versions()
    print(versions)
    return versions


def get_latest_lambda_versions():
    versions = []
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(S3_SOURCE_BUCKET)
    for lambda_zip in os.listdir("build/lambdas"):
        if ".zip" not in lambda_zip:
            continue
        latest_version = bucket.object_versions.filter(
            Prefix="{}/{}".format(MATURITY, "send_email.zip"),
            MaxKeys=1
        )[0]
        versions.append((
            lambda_zip[:-4],
            latest_version.id
        ))

    return versions


def post_build():
    bucket_uri = "s3://{}".format(
        os.path.join(BUCKET_BASE_DIR, "config/configuration.json")
    )

    subprocess.check_call(["aws", "s3", "cp", bucket_uri, "build/"])
    subprocess.check_call([
        "aws", "s3", "cp", "docs/_build/html",
        "s3://asf-docs/hyp3-in-a-box",
        "--recursive", "--acl", "public-read"
    ])
    set_github_ci_status("success", description=get_config(
        "TEST_RESULT_SUMMARY", "Build completed"))


def install_all_requirements_txts(root_dir):
    for path, dirs, files in os.walk(root_dir):
        for name in files:
            if "requirements" in name:
                subprocess.check_call(
                    ["pip", "install", "-U", "-r", name],
                    cwd=path
                )


def save_config(key, value):
    if os.path.exists("/tmp/config.json"):
        with open("/tmp/config.json", "r+") as f:
            config = json.load(f)
            config[key] = value
            f.seek(0)
            json.dump(config, f)
    else:
        with open("/tmp/config.json", "w") as f:
            json.dump({key: value}, f)


def get_config(key, default=None):
    try:
        with open("/tmp/config.json", "r") as f:
            config = json.load(f)
            return config.get(key, default)
    except FileNotFoundError:
        return default


def main(step=None):
    if not os.path.exists("build"):
        os.mkdir("build")

    step_function_table = {
        "install": install,
        "pre_build": pre_build,
        "build": build,
        "post_build": post_build
    }

    try:
        if get_config("BUILD_STATUS", 0) == 0:
            save_config("BUILD_STATUS", 0)
            return step_function_table.get(step, lambda: None)()
    except subprocess.CalledProcessError as e:
        desc = step
        if 'failure' in BUILD_STEP_MESSAGES is not None:
            desc = BUILD_STEP_MESSAGES['failure']
        set_github_ci_status("failure", description=desc)
        save_config("BUILD_STATUS", e.returncode)
        raise
    except Exception:
        set_github_ci_status("error")
        save_config("BUILD_STATUS", -1337)
        raise


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(step=sys.argv[1])
    else:
        main()
