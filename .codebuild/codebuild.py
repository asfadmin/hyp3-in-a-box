# codebuild.py
# Rohan Weeden, William Horn
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

import github

# Use SemVer!
RELEASE_VERSION = "0.2.1"

TEMPLATE_CONFIG_BUCKET = "hyp3-in-a-box"
TEMPLATE_NAME = 'hyp3-in-a-box_US-EAST-1v{}.json'.format(RELEASE_VERSION)


S3_SOURCE_BUCKET = os.environ["S3_SOURCE_BUCKET"]
MATURITY = os.environ["MATURITY"]
GITHUB_ASFADMIN_CLONE_TOKEN = os.environ["GITHUB_HYP3_API_CLONE_TOKEN"]
BUCKET_BASE_DIR = os.path.join(
    S3_SOURCE_BUCKET,
    "releases/{}/".format(RELEASE_VERSION) if MATURITY == "prod" else MATURITY + "/")
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

        step_fn = step_function_table.get(step, lambda: None)
        print(f'Starting {step_fn.__name__}:')

        return step_fn()

    except subprocess.CalledProcessError as e:
        desc = BUILD_STEP_MESSAGES.get("failure", step)

        github.set_github_ci_status("failure", description=desc)
        save_config("BUILD_STATUS", e.returncode)
        raise
    except Exception:
        github.set_github_ci_status("error")
        save_config("BUILD_STATUS", -1337)
        raise


def install():
    github.update_github_status("pending", description="Build in progress")
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
    cov_xml_path = pl.Path("/tmp/cov.xml")
    test_results = pl.Path("/tmp/test_results.xml")

    try:
        subprocess.check_call([
            "py.test", "-n", "auto",
            "--junitxml={}".format(test_results),
            "--cov=.", "--cov-report",
            "xml:{}".format(cov_xml_path), "-s", "."
        ])
        check_coverage(cov_xml_path)
    except subprocess.CalledProcessError as e:
        raise e
    finally:
        r = ElementTree.parse(str(test_results)).getroot()
        test_result_summary = "{} Tests, {} Failed, {} Errors".format(
            int(r.get("tests", 0)) - int(r.get("skips", 0)),
            r.get("failures"),
            r.get("errors")
        )
        BUILD_STEP_MESSAGES["failure"] = test_result_summary
        save_config("TEST_RESULT_SUMMARY", test_result_summary)


def check_coverage(cov_xml_path):
    r = ElementTree.parse(str(cov_xml_path)).getroot()
    coverage = float(r.get("line-rate"))
    coverage_percent = int(coverage * 100)

    url_percent_sign = "%25"
    subject, status = "coverage", "{}{}".format(
        coverage_percent, url_percent_sign)
    color = get_badge_color(coverage)

    github.write_status_to_s3(subject, status, color)


def get_badge_color(coverage):
    if coverage < .65:
        color = "red"
    elif coverage < .80:
        color = "yellow"
    else:
        color = "brightgreen"

    return color


class Build(object):

    def __init__(self):
        self.release_options = []
        self.lambda_key_prefix = MATURITY
        self.template_key = "template/{}".format(TEMPLATE_NAME)
        self.template_acl = "bucket-owner-full-control"

    def build(self):
        os.makedirs("build/lambdas")
        self.build_lambdas()
        object_versions = self.get_latest_lambda_versions()

        print("Latest Source Versions:")
        print(object_versions)

        version_options = []
        for v in object_versions:
            print(f'adding object version {v}')
            version_options += ["--{}_version".format(v[0]), v[1]]

        self.build_hyp3_api()

        template_path = 'build/template.json'
        subprocess.check_call([
            "python3", "cloudformation/tropo/create_stack.py",
            template_path, "--maturity", MATURITY, "--source_bucket", S3_SOURCE_BUCKET
        ] + version_options + self.release_options
        )
        subprocess.check_call(["make", "clean", "html"], cwd="docs")

        self.upload_template(template_path)
        self.make_release()

    # pylint: disable=R0201
    def build_lambdas(self):
        subprocess.check_call([
            "python3", "lambdas/build_lambda.py", "-a",
            "-o", "build/lambdas/", "lambdas/"
        ])

    def get_latest_lambda_versions(self):
        versions = []
        s3 = boto3.resource("s3")
        bucket = s3.Bucket(S3_SOURCE_BUCKET)
        prefix = self.lambda_key_prefix

        for lambda_zip in os.listdir("build/lambdas"):
            if ".zip" not in lambda_zip:
                continue

            latest_versions = bucket.object_versions \
                .filter(
                    Prefix="{}/{}".format(prefix, lambda_zip),
                    MaxKeys=1
                ).limit(count=1)

            versions += [(lambda_zip[:-4], v.id) for v in latest_versions]

        print(f'found lambda versions: {versions}')

        return versions

    # pylint: disable=R0201
    def build_hyp3_api(self):
        print('building hyp3 api')
        hyp3_api_url = "https://{}@github.com/asfadmin/hyp3-api".format(
            GITHUB_ASFADMIN_CLONE_TOKEN
        )

        print('cloning hyp3 api')
        subprocess.check_call([
            "git", "clone", hyp3_api_url, "--depth", "1"
        ])
        api_flask_path = pl.Path('hyp3-api/hyp3-flask')

        print(f"HyP3 api directories: {os.listdir(str(api_flask_path))}")
        subprocess.check_call([
            "zip", "-r", "../../build/hyp3_api.zip", "."],
            cwd=str(api_flask_path)
        )

    def upload_template(self, file_path):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(S3_SOURCE_BUCKET)
        key = self.template_key

        with open(file_path, 'rb') as f:
            return bucket.put_object(
                Key=key,
                Body=f,
                ACL=self.template_acl
            )

    def make_release(self):
        pass


class ProdBuild(Build):
    def __init__(self):
        super().__init__()
        ProdBuild.check_release_exists()
        self.release_options = ["--release", RELEASE_VERSION]
        self.lambda_key_prefix = "releases/{}".format(RELEASE_VERSION)
        self.template_key = "releases/{}/{}".format(
            RELEASE_VERSION, TEMPLATE_NAME)
        self.template_acl = "public-read"

    def make_release(self):
        github.create_release(RELEASE_VERSION)

    @staticmethod
    def check_release_exists():
        try:
            subprocess.check_output([
                "aws", "s3api", "head-object", "--bucket",
                "asf-hyp3-in-a-box-source-east", "--key",
                "releases/{}/{}".format(RELEASE_VERSION, TEMPLATE_NAME)
            ])
            raise Exception(
                "Version {} already exists!".format(RELEASE_VERSION)
            )
        except subprocess.CalledProcessError as e:
            if e.returncode != 255:
                raise e
            print("Current release was not found... good")


def build():
    builder = ProdBuild() if MATURITY == "prod" else Build()
    builder.build()


def post_build():
    bucket_uri = "s3://{}".format(os.path.join(
        TEMPLATE_CONFIG_BUCKET, MATURITY, "config/configuration.json"
    ))

    subprocess.check_call(
        ["aws", "s3", "cp", bucket_uri, "build/"] + get_s3_acl_cmd())

    print("Uploading lambdas")
    subprocess.check_call([
        "aws", "s3", "cp", "build/lambdas",

        "s3://{}".format(BUCKET_BASE_DIR),
        "--recursive",
        "--include", '"*"'
    ] + get_s3_acl_cmd())
    print(f'uploading api to {BUCKET_BASE_DIR}')
    subprocess.check_call([
        "aws", "s3", "cp", "build/hyp3_api.zip",
        "s3://{}".format(BUCKET_BASE_DIR)
    ] + get_s3_acl_cmd())
    subprocess.check_call([
        "aws", "s3", "cp", "docs/_build/html",
        get_docs_folder(),
        "--recursive", "--acl", "public-read"
    ])

    if MATURITY == "prod":
        subprocess.check_call([
            "aws", "s3", "cp",
            "s3://{}/data/default-processes.json".format(S3_SOURCE_BUCKET),
            "s3://{}/releases/{}/data/default-processes.json".format(
                S3_SOURCE_BUCKET, RELEASE_VERSION),
            "--acl", "public-read"
        ])
    github.set_github_ci_status("success", description=get_config(
        "TEST_RESULT_SUMMARY", "Build completed"))


def get_docs_folder():
    folder = "s3://asf-docs/hyp3-in-a-box"
    if MATURITY == "prod":
        folder += "/releases/{}".format(RELEASE_VERSION)
    else:
        folder += "/test"
    return folder


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


def get_s3_acl_cmd():
    permissions = []
    if MATURITY == "prod":
        permissions = ["--acl", "public-read"]
    return permissions


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(step=sys.argv[1])
    else:
        main()
