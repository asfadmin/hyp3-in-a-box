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

Earthdata Credentials
^^^^^^^^^^^^^^^^^^^^^

    To download data within HyP3, an Earthdata account is needed.
    To create an Earthdata account go to:

        - `Register for Earthdata`_

    **NOTE:** Make sure that all the required EULA's are excepted on your
    Earthdata account or else HyP3 will not be able to successfully download
    data.

    The username and password for this account will be used later when
    creating the CloudFormation stack.

Launching the CloudFormation stack
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   Once you have a key pair, and have verified an email with SES, you're ready to
   create the CloudFormation stack. This automatically generates and configures all
   of the AWS resources HyP3 needs.

   The template is bound to a specific region referenced in the name.
   The naming convention for the template is as follows:

      ``hyp3-in-a-box_<aws region here>.json``

   Be sure to create the template in the correct region or the template will no work.
   Currently the only supported region is ``us-east-1``.

Stack Parameters
~~~~~~~~~~~~~~~~

    The ``authorized email``, ``ec2-key-pair`` and ``earhtdata credentials`` from the
    previous steps will be used here.

    All the parameters that have default values can be left unchanged.

    Passwords for the database must also be passed in as parameters. These should be secure
    and only contain alphanumeric characters.  `random.org`_ is a good website for doing just that.

    The HyP3 email and username must be added. This will where the notifications get sent and the
    username will be used for accessing with the HyP3. The HyP3 email can be different from the verified
    email but both must be entered.

    The maximum number of running instances determines how many servers can run processing
    at one time. Increasing this number will affect how much AWS charges, but allows you
    to process more data.

    The Api cidr range is to limit access to the api. The default (0.0.0.0/0) allows all traffic through.

    Solution stack name it the elastic beanstalk. To find then newest version go here:

        - `Elastic Beanstalk Solution Stack`_.

    Pick the latest python 3.6 solution stack name.

Launching
~~~~~~~~~

    To launch the cloudformation stack

    * Download a version of the HyP3 cloudformation template: :ref:`releases`.
    * Login to the **AWS conosle**.
    * Go to the **Cloudformation** section and click **Create Stack**.
    * Under **Choose a template**, select the option to **upload a file**.
    * **Upload** the HyP3 CloudFormation template then hit **next**.
    * Give the stack a name and **fill in the missing parameters**.
    * Hit next again, then click the checkbox to **allow IAM** and hit create!

    When stack is finished creating you're ready to start using HyP3! Using the api,
    which is linked in stack outputs, create a subscription over your area of interest
    and start receiving data. The username and api-key for the newly created HyP3 API is stored
    in AWS `Systems Manager`_ parameter store.

Creating A Subscription
~~~~~~~~~~~~~~~~~~~~~~~

    To start processing data, a subscription needs to be created. Navigate to the HyP3 API website,
    the URL for the API is in outputs of the stack. Click on ``create_subscription`` and fill out the
    subscription form. An example subscription will look something like this:

    .. image:: ../_static/images/example-subscription.png
       :alt: alternate text
       :align: right


    Change the ``location`` parameter to be a valid WKT Multipolygon over your area of intrest.

    Possible process_id's can be found py running a get_processes api call. The ``Username`` and ``API Key``
    can also be found as stack outputs.

    **Note:** Currently ``platform`` and ``crop_to_selection`` are not implimented, so they have no effect.
    They must still be entered because of the api, parameter validation.


.. _Generate Ec2 Key Pairs: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html
.. _Verify Your Email: https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses-procedure.html?shortFooter=true
.. _random.org: https://www.random.org/passwords/
.. _Systems Manager: https://aws.amazon.com/systems-manager/
.. _Register for Earthdata: https://urs.earthdata.nasa.gov/profile/
.. _Elastic Beanstalk Solution Stack: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.platforms.html#concepts.platforms.python
