.. _setup:

Installation
============

Generate an EC2 Key Pair
^^^^^^^^^^^^^^^^^^^^^^^^

    HyP3 uses Elastic Coumput Cloud (EC2) instances to processes data. To have access to
    these instances an ``EC2 Key Pair`` is needed. To generate an EC2 Key pair follow this tutorial:

        - `Generate EC2 Key Pairs`_.

    The created key pair will be used as a parameter in the cloudformation template.

Authorize an email address in SES
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Email notifications are sent using Amazon's Simple Email Service (SES).
    Only ``verified emails`` are allowed to send emails using this service.
    To veriry your email, follow this tutorial:

        - `Verify Your Email`_.

    This email will also be used as a parameter in the template

Launching the CloudFormation stack
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   Once you have a key pair, and have verified an email with SES, your ready to
   create the cloudformation stack. This automatically generates and configures all
   of the aws resources HyP3 needs.

   The template is bound to a specific region referenced in the name.
   The naming convension for the template is as follows:

      ``hyp3-in-a-box_<aws region here>.json``

   Be sure to create the template in the correct region or the template will no work.
   Currently the only supported region is ``us-west-2``.

Stack Parameters
~~~~~~~~~~~~~~~~

    The ``authorized email`` and ``ec2-key-pair`` from the previous steps will be used here.

    All the parameters that can have default values can be left unchanged.

    Passwords for the database must also be passed in as parameters. These should be secure
    and only contain alphanumeric characters.  `random.org`_ is a good website for doing just that.

    The hyp3 email and username must be added. This will where the notifications get sent and the
    username will be used for accessing with the hyp3. The hyp3 email can be different from the verified
    email but both must be entered.

Launching
~~~~~~~~~

    To launch the cloudformation stack

    * Download a version of the hyp3 cloudformation template: :ref:`releases`.
    * Login to the **AWS conosle**.
    * Go to the **Cloudformation** section and click **Create Stack**.
    * Under **Choose a template**, select the option to **upload a file**.
    * **Upload** the hyp3 CloudFormation template then hit **next**.
    * Give the stack a name and **fill in the missing parameters**.
    * Hit next again, then click the checkbox to **allow IAM** and hit create!

    When stack is finished creating your ready to start using HyP3! Using the api,
    which is linked in stack ouptuts, create a subscription over your area of intreset
    and start recieving data. The username and api-key for the newly created HyP3 API is stored
    in AWS `Systems Manager`_ parameter store.

Basic Usage
~~~~~~~~~~~

.. _Generate Ec2 Key Pairs: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html
.. _Verify Your Email: https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses-procedure.html?shortFooter=true
.. _random.org: https://www.random.org/password/
.. _Systems Manager: https://aws.amazon.com/systems-manager/
