# HyP3 in a Box!

| Build Status          |                                       |
| --------------------- | ------------------------------------- |
| **Test** | ![Build Status](https://s3-us-west-2.amazonaws.com/asf-docs/hyp3-in-a-box/test-build-status.svg) ![Build Status](https://s3-us-west-2.amazonaws.com/asf-docs/hyp3-in-a-box/test-coverage-status.svg) |
| **Prod** | ![Build Status](https://s3-us-west-2.amazonaws.com/asf-docs/hyp3-in-a-box/prod-build-status.svg) |


Documentation on hyp3-in-a-box project can be found [here](http://asf-docs.s3-website-us-west-2.amazonaws.com/hyp3-in-a-box/test/)

## Troposphere
We are using `troposphere` for easier creation of the CloudFormation template.
The main advantage here is that we can logically separate parts of the template
into multiple files e.g. a file for the database, a file for each lambda function
etc. Troposphere also does some template validation, so it guarantees that if
a template is generated, it will be valid.

## Tests
We use `pytest` to run all unit tests in the project. This means sometimes we
need to do hacky things with the import paths to make sure the tests can be run
from the root directory of the project.

We have also set up a scratch database for unit testing (appropriately named
`unit-testing`). The hostname is
`unit-testing.cxpvv5ynyjaw.us-west-2.rds.amazonaws.com` and credentials are
```
user: unittest
pass: unittestpass
```
*Don't store any confidential info in this database. Assume that anyone can log
in to it and only use it for testing.*

For the purposes of our unit tests we assume that when we connect to the db, it
may contain left over tables and content from a different test, so our test
suites will drop and recreate the database that they need.

The security group for this database is configured to only allow access from
inside the default VPC and from UAF IP addresses.

## CI Configuration
This project is set up to build and test using AWS CodeBuild. CodeBuild uses
WebHooks for change detection on the `dev` branch. We do most of the automation
in the `.codebuild/codebuild.py` script which is run in each stage of the build
process. Each build will perform the following steps:

1.  Install Dependencies
2.  Run Unit Tests
3.  Generate CloudFormation template
4.  Bundle lambda zip files
5.  Generate and upload sphinx documentation

We also set up some GitHub status reporting using the GitHub API. This requires
a GitHub access token for any user with access to the repository. You can
generate an access token by going to `Settings > Developer Settings > Personal
Access Tokens` more on how GitHub access tokens work here:
 [https://developer.github.com/v3/#authentication](https://developer.github.com/v3/#authentication).
To get CodeBuild to use the access token, configure the CodeBuild project
settings to pass it in as an environment variable called `GITHUB_STATUS_TOKEN`.
The best way to keep this token secure is to use the `Parameter Store` option.

### Environment Variables

| Name                | Description                                            |
| ------------------- | ------------------------------------------------------ |
| MATURITY            | Used for bucket folder names and file name prefixes    |
| GITHUB_STATUS_TOKEN | Used to set commit status. Omitting this will not change the result of the build, API calls will fail silently |

### Build Scripts
There are a few scripts in this repository that CodeBuild uses to build certain
elements of the project. These scripts can also be used manually (outside of the
CI context).

#### build_lambda.py
**located in:** lambdas/

Creates a zip file containing lambda function source code and dependencies.
Assumes that lambda function directories follow a particular structure:

1.  Must contain a `src` directory
2.  Must contain a `requirements.txt` file

Requirements will be pre-compiled and installed with pip to a `dependencies`
folder in the lambda function directory. Any modules installed to the
`dependencies` folder will be included in the final zip file, so if you need to
include modules which cannot be installed with pip, just drop the files in there.

#### create_stack.py
**located in:** cloudformation/tropo/

Generates a CloudFormation json template from the troposphere files. Can be used
to include only some of the HyP3 components (use `--help` for more information).

#### upload.sh
**located in:** /

A slightly misleading name. This script actually generates the sphinx
documentation and uploads it to the asf-docs s3 bucket using the aws cli. You
will need to have the cli installed and bucket write permissions.
