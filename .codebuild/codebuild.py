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
import pathlib as pl

from defusedxml import ElementTree

import boto3

import github_status as gs

S3_SOURCE_BUCKET = "asf-hyp3-in-a-box-source"
MATURITY = os.environ["MATURITY"]
GITHUB_HYP3_API_CLONE_TOKEN = os.environ["GITHUB_HYP3_API_CLONE_TOKEN"]
BUCKET_BASE_DIR = os.path.join(S3_SOURCE_BUCKET, MATURITY + "/")
BUILD_STEP_MESSAGES = {}


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
        if get_config("BUILD_STATUS", 0) != 0:
            return None

        save_config("BUILD_STATUS", 0)

        step = step_function_table.get(step, lambda: None)
        print(f'Starting {step.__name__}:')

        return step()

    except subprocess.CalledProcessError as e:
        desc = step
        if "failure" in BUILD_STEP_MESSAGES is not None:
            desc = BUILD_STEP_MESSAGES["failure"]

        gs.set_github_ci_status("failure", description=desc)
        save_config("BUILD_STATUS", e.returncode)
        raise
    except Exception:
        gs.set_github_ci_status("error")
        save_config("BUILD_STATUS", -1337)
        raise


def install():
    gs.update_github_status("pending", description="Build in progress")
    install_all_requirements_txts(".")
    os.chmod("upload.sh", stat.S_IEXEC)


def install_all_requirements_txts(root_dir):
    for path, dirs, files in os.walk(root_dir):
        for name in files:
            if "requirements" in name:
                subprocess.check_call(
                    ["pip", "install", "-U", "-r", name],
                    cwd=path
                )


def pre_build():
    run_tests()


def run_tests():
    try:
        subprocess.check_call(
            ["python3", "-m", "pytest", "--junitxml=/tmp/test_results.xml"])
    except subprocess.CalledProcessError as e:
        raise e
    else:
        check_coverage()
    finally:
        r = ElementTree.parse("/tmp/test_results.xml").getroot()
        test_result_summary = "{} Tests, {} Failed, {} Errors".format(
            int(r.get("tests", 0)) - int(r.get("skips", 0)),
            r.get("failures"),
            r.get("errors")
        )
        BUILD_STEP_MESSAGES["failure"] = test_result_summary
        save_config("TEST_RESULT_SUMMARY", test_result_summary)


def check_coverage():
    cov_xml_path = pl.Path("/tmp/cov.xml")
    subprocess.check_call(
        ["py.test", "--cov=.", "--cov-report",
            "xml:{}".format(cov_xml_path), "."]
    )

    r = ElementTree.parse(str(cov_xml_path)).getroot()
    coverage = float(r.get("line-rate"))
    coverage_percent = int(coverage * 100)

    url_percent_sign = "%25"
    subject, status = "coverage", "{}{}".format(
        coverage_percent, url_percent_sign)
    color = get_badge_color(coverage)

    gs.write_status_to_s3(subject, status, color)


def get_badge_color(coverage):
    if coverage < .65:
        color = "red"
    elif coverage < .80:
        color = "yellow"
    else:
        color = "brightgreen"

    return color


def build():
    os.makedirs("build/lambdas")
    object_versions = build_lambdas()

    version_options = []
    for v in object_versions:
        print(f'adding object version {v}')
        version_options += ["--{}_version".format(v[0]), v[1]]

    build_hyp3_api()

    template_path = 'build/template.json'
    subprocess.check_call([
        "python3", "cloudformation/tropo/create_stack.py",
        template_path, "--maturity", MATURITY
    ] + version_options
    )
    subprocess.check_call(["make", "clean", "html"], cwd="docs")

    upload_template(template_path)


def upload_template(file_path):
    s3 = boto3.resource('s3')

    key = 'template/hyp3-in-a-box-template.json'
    bucket = s3.Bucket(S3_SOURCE_BUCKET)

    with open(file_path, 'rb') as f:
        return bucket.put_object(
            Key=key,
            Body=f
        )


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
    versions = get_latest_lambda_versions()

    print("Latest Source Versions:")
    print(versions)

    return versions


def get_latest_lambda_versions():
    versions = []
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(S3_SOURCE_BUCKET)
    for lambda_zip in os.listdir("build/lambdas"):
        if ".zip" not in lambda_zip:
            continue

        latest_versions = bucket.object_versions \
            .filter(
                Prefix="{}/{}".format(MATURITY, lambda_zip),
                MaxKeys=1
            ).limit(count=1)

        versions += [
            (lambda_zip[:-4], v.id) for v in latest_versions
        ]

    print(f'found lambda versions: {versions}')

    return versions


def build_hyp3_api():
    print('building hyp3 api')
    hyp3_api_url = "https://{}@github.com/asfadmin/hyp3-api".format(
        GITHUB_HYP3_API_CLONE_TOKEN
    )

    print('cloning hyp3 api')
    subprocess.check_call([
        "git", "clone", hyp3_api_url, "--depth", "1"
    ])
    api_flask_path = pl.Path('hyp3-api/hyp3-flask')

    api_cfg_path = "s3://{}".format(
        os.path.join(BUCKET_BASE_DIR, "config/hyp3_api_config.json")
    )
    subprocess.check_call([
        "aws", "s3", "cp", api_cfg_path, str(api_flask_path / "config.json")
    ])

    print(f"Hyp3 api directories: {os.listdir(str(api_flask_path))}")
    subprocess.check_call([
        "zip", "-r", "../build/hyp3_api.zip", str(api_flask_path.name)],
        cwd=str(api_flask_path.parent)
    )

    print(f'uploading to {BUCKET_BASE_DIR}')
    subprocess.check_call([
        "aws", "s3", "cp", "build/hyp3_api.zip",
        "s3://{}".format(BUCKET_BASE_DIR)
    ])


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
    gs.set_github_ci_status("success", description=get_config(
        "TEST_RESULT_SUMMARY", "Build completed"))


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


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(step=sys.argv[1])
    else:
        main()
