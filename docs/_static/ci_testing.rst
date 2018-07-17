.. _ci_testing:

Continuous Integration
======================

Continuous integration for HyP3-In-A-Box is done using AWS `CodePipeline`_. Pushing to the
dev branch triggers the build. Before building the `Cloudformation`_ template the tests are
run and the build will only succeed if all the tests pass.

The lambdas are zipped up into a public versioned `S3`_ and a `Cloudformation`_ template is generated
using the specific version number just uploaded to `S3`_. This allows for templates to have deterministic
builds that are not dependent on being in a specific AWS account.

Testing
-------

Test are run using `pytest`_, the requirements files in each sub-folder is installed because `pytest`_
needs to have everything imported to run the full test suit. Test coverage is done using the `pytest-cov`_
plugin for `pytest`_. This generates an xml file describing the test coverage which is used to create a badge
to show the test coverage percentage. Tests are run in parallel using another `pytest`_ plugin called `pytest-xdist`_.

Monitoring
----------

A custom `CloudWatch`_ dashboard is created with the template. It shows real time data for all the lambda
functions in the system as well as the HyP3 `RDS`_ database.

.. _pytest: https://docs.pytest.org/en/latest/
.. _CodePipeline: https://aws.amazon.com/codepipeline/
.. _Cloudformation: https://aws.amazon.com/cloudformation/
.. _S3: https://aws.amazon.com/s3/
.. _RDS: https://aws.amazon.com/rds/
.. _CloudWatch: https://aws.amazon.com/cloudwatch/
.. _pytest-cov: https://pytest-cov.readthedocs.io/en/latest/
.. _pytest-xdist: https://github.com/pytest-dev/pytest-xdist
