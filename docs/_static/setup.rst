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
successfully. Further details on each of these steps will be available in the
following sections.

1. Zip Lambda code/dependencies and upload to an S3 Bucket
2. Generate an EC2 Key Pair
3. Authorize an email address in SES
4. Generate the CloudFormation template
5. Launch a new stack from the CloudFormation template

1. Zipping Lambda Code With Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Note:** `You do not need to do this step if you have the prebuilt zip files
provided by ASF.`

Building AWS Lambda function source bundles is as simple as zipping up the
source code. However, if the code has any external dependencies, those must also
be included in the zip file, as Lambda will not install dependencies at run
time. For creating the HyP3 Lambdas you can use the :ref:`build_lambda_script`
helper script.

To build all lambda functions in the ``lambdas/`` directory:
  1. cd hyp3-in-a-box/
  2. mkdir -p build/lambdas
  3. python3 build_lambda.py -a -o build/lambdas/ lambdas/

This command will tell ``build_lambda.py`` to look through the ``lambdas/``
directory and bundle the source for each lambda along with any dependencies
defined in the ``requirements.txt`` file into a zip file and place it into the
``build/lambdas/`` directory. This also handles the special case for the
``psycopg2`` package which needs to be specially built for AWS Lambda.

2. Generating an EC2 Key Pair
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

4. Generating the CloudFormation template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

5. Launching the CloudFormation stack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _AWS Key Pair Documentation: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html
