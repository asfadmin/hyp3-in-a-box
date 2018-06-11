# HyP3 in a Box !

| Build Status ||
| --------------------- | ------------------------------------- |
| **Test** | ![Build Status](https://s3-us-west-2.amazonaws.com/asf-docs/hyp3-in-a-box/test-build-status.svg) |
| **Prod** | ![Build Status](https://s3-us-west-2.amazonaws.com/asf-docs/hyp3-in-a-box/prod-build-status.svg) |


Documentation on hyp3-in-a-box project can be found [here](http://asf-docs.s3-website-us-west-2.amazonaws.com/hyp3-in-a-box/)

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

## CI Configuration
This project is set up to build and test using AWS CodeBuild. CodeBuild uses
WebHooks for change detection on the `dev` branch. We do most of the automation
in the `.codebuild/codebuild.py` script which is run in each stage of the build
process. Each build will perform the following steps:

1.  Install Dependencies
2.  Run Unit Tests
3.  Generate CloudFormation template
4.  Bundle lambda zip files
5.  Generate and upload sphynx documentation

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
| GITHUB_STATUS_TOKEN | Used to set commit status. Omitting this will not change the result of the build, API calls will fail silently  |
