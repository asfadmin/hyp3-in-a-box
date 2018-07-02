.. _setup:

Setup In Your Own AWS Account
=============================

Getting HyP3 up and running in your own AWS account is made relatively simple
through CloudFormation templates. The majority of the work will be taken care of
for you, however, some of the configuration options (such as the SES Authorized
email to send notifications from) will require you to do some preparation before
being able to create the CloudFormation stack.

Overview
--------

Here is an outline of the steps required to get the HyP3 stack running
successfully. Our goal is to make this list as short as possible. Further
details on each of these steps will be available in the following sections.

1. Zip Lambda code/dependencies and upload to an S3 Bucket
2. Generate an EC2 Key Pair
3. Authorize an email address in SES
4. Generate the CloudFormation template
5. Launch a new stack from the CloudFormation template

Optional
~~~~~~~~
6. Enable EarthData login for the HyP3 API
7. Enable HTTPS on the HyP3 API (`recommended`)

1. Zipping Lambda Code With Dependencies
----------------------------------------

**Note:** `You can skip the zipping step if you have the prebuilt zip files
provided by ASF. However, you will still need to upload them to your own S3
Bucket.`

Building AWS Lambda function source bundles is as simple as zipping up the
source code. However, if the code has any external dependencies, those must also
be included in the zip file, as Lambda will not install dependencies at run
time. For creating the HyP3 Lambdas you can use the :ref:`build_lambda_script`
helper script.

To build all lambda functions in the ``lambdas/`` directory:
  1. ``cd hyp3-in-a-box/``
  2. ``mkdir -p build/lambdas``
  3. ``python3 build_lambda.py -a -o build/lambdas/ lambdas/``

This command will tell ``build_lambda.py`` to look through the ``lambdas/``
directory and bundle the source for each lambda along with any dependencies
defined in the ``requirements.txt`` file into a zip file and place it into the
``build/lambdas/`` directory. This also handles the special case for the
``psycopg2`` package which needs to be specially built for AWS Lambda.

Upload to S3
~~~~~~~~~~~~
You will need to store the source code for the lambda functions in an S3 Bucket
`in the same region as the rest of the HyP3 system`. If the bucket is not in the
same region, CloudFormation will fail to locate it.

1. Create an S3 bucket named ``your-organization-hyp3-source``
2. Create a folder called ``prod/``
3. Upload each of the lambda zip files into the ``prod/`` folder

You must upload the zip files prior to launching the CloudFormation stack, as
CloudFormation will attempt to create the components of HyP3 using the source
packages in this bucket.

2. Generating an EC2 Key Pair
-----------------------------

In order to connect to a running EC2 instance you will need to generate an SSH
key pair. When an EC2 instance is launched with a key pair, AWS places the
public key in the instance's ``authorized_keys`` file, allowing you to connect
via SSH with the associated private key.

If you have a key pair already, you may want to use that for the HyP3 stack as
well, or you could generate a new key just for HyP3. Either way, make sure you
have access to the private key file, so that you are able to diagnose the
processing instances on the off chance that they experience any issues.

Key pairs are created in the
`EC2 management console <https://console.amazonaws.com/ec2>`_. Go to ``Network
& Security`` > ``Key Pairs`` and click "Create Key Pair".

.. image:: images/create_key_pair.png
   :alt: Create Key Pair Image

Enter a meaningful name and hit "Create".

.. image:: images/create_key_pair_confirm.png
   :alt: Create Key Pair Image

Make sure you save the private key ``.pem`` file as this is the only time you
will be able to download it. Amazon only stores the public key. It's also a good
idea to save this file to the ``.ssh`` folder in your home directory and to set
the permissions to be readable only by you with
``sudo chmod 0400 ~/.ssh/mykey.pem``.

For more information see the official `AWS Key Pair Documentation`_.

3. Authorizing an email for SES
-------------------------------

There are 2 steps to fully authorizing an email address with Amazon. First you
will need to verify that you own the email address through the
`SES management console <https://console.amazonaws.com/ses>`_. Go to ``Email
Addresses`` and click "Verify a New Email Address". Enter the email address
which HyP3 will use to send notification emails once new data is available and
click "Verify This Email Address". Amazon will send an email containing a
verification link to this address.

.. image:: images/verify_email.png
   :alt: Verify Email Image

This will allow you to send emails `to` the HyP3 email address, but your account
will likely still be in sandbox mode, preventing you from sending emails to any
non verified addresses. This is to prevent email spammers from abusing SES.

To get the sandbox restriction removed from your account, you will need to open
a sending limit increase request with the Support Center. This request will both
allow your account to get out of sandbox mode, and increase the daily email
limit of 200 emails every 24 hours.

We recommend that you request a limit of at least 50 emails per expected
subscription (across all users). So if you expect to have 10 users with 10
subscriptions each, you should request a rate limit of at least
``10 * 10 * 50 = 5000``. In future iterations of the HyP3 system this number may
be lower as we work on implementing a notification accumulator, which will
combine notifications which occur close to each other into a single email.

For more details on opening the Support Center sending limit increase request
see the official `AWS Removing SES Sandbox Documentation`_.

4. Generating the CloudFormation template
-----------------------------------------

You can generate the template using the ``create_stack.py`` script located in
``cloudformation/tropo/``. The script requires a few dependencies which you can
install to a virtual environment.

**Note:** `You will need Python 3 to create the template! Make sure your
virtual environment is using Python 3.`

1. ``cd cloudformation``
2. ``virtualenv -p python3 .venv``
3. ``source .venv/bin/activate``
4. ``pip install -r requirements.txt``
5. ``python3 tropo/create_stack.py --lambda_bucket MY_BUCKET --eb_bucket MY_BUCKET --maturity prod tropo/outputs/hyp3_stack.json``

Make sure that ``MY_BUCKET`` is the bucket you created in step 1 which contains
all of the source code for the HyP3 components. Also make sure that the maturity
matches the name of the folder that you placed the bundles into.

The resulting template will be written to ``tropo/outputs/hyp3_stack.json``. You
can now use this to launch your own HyP3 stack.

**Note:** `If you will be launching the stack programmatically or through the
AWS CLI, you will need a configuration.json file. You can create this by passing
the` ``--config`` `option to` ``create_stack.py``.

5. Launching the CloudFormation stack
-------------------------------------

.. _AWS Key Pair Documentation: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html
.. _AWS Removing SES Sandbox Documentation: https://docs.aws.amazon.com/ses/latest/DeveloperGuide/request-production-access.html
