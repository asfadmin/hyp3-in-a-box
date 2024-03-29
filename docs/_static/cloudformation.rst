.. _cloudformation:

AWS CloudFormation
==================

.. image:: images/cloudformation.png
   :alt: alternate text
   :align: right

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   cloudformation/find_new.rst
   cloudformation/send_email.rst
   cloudformation/scheduler.rst
   cloudformation/setup_db.rst
   cloudformation/custom_metric.rst

   cloudformation/rds.rst
   cloudformation/api_eb.rst
   cloudformation/vpc.rst

   cloudformation/s3.rst
   cloudformation/sns.rst
   cloudformation/sqs.rst
   cloudformation/autoscaling_group.rst

   cloudformation/kms_key.rst
   cloudformation/db_params.rst
   cloudformation/keypair_name_param.rst

   cloudformation/ec2_userdata.rst
   cloudformation/dashboard.rst

Troposphere
-----------

`Troposphere`_ is a python library for generating CloudFormation templates.
It is a lightweight wrapper around CloudFormation which allows for a more
dynamic environment than plain JSON.

.. _Troposphere: https://github.com/cloudtools/troposphere

Template Generation
-------------------

The ``create_stack.py`` script is used to generate the raw CloudFormation JSON.
It can generate the full template, or include only some resources for testing
purposes.

.. code-block:: bash

   python create_stack.py --find_new --api_eb outputs/template.json

This command makes a template with the :ref:`find_new_lambda` lambda and the
Elastic Beanstalk application that runs the API. Note that it will also include
the VPC template because the Elastic Beanstalk application depends on it.

Environment variables can also be dynamically set using the ``create_stack``
script. This is an example of changing which bucket lambda functions get pulled
from and setting the maturity of the template to ``test`` while only making
:ref:`send_email_lambda`.

.. code-block:: bash

   python create_stack.py                  \
       --send_email                        \
       --lambda_bucket some-s3-bucket-name \
       --maturity test                     \
       outputs/template.json

Add environment variables to the Environment class's __init__ function.

Troposphere Templates
---------------------

Each file in ``cloudformation/tropo/templates`` directory is responsible for
creating a logical portion of the Hy3P-In-A-Box infrastructure. Each flag in
``create_stack.py`` corresponds to one of these file.
