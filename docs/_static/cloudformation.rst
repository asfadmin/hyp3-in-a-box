.. hyp3_api_eb.py  hyp3_find_new.py  hyp3_rds.py  hyp3_send_email.py  hyp3_vpc.py

.. _cloudformation:

AWS CloudFormation
==================

.. image:: images/cloudformation.png
   :alt: alternate text
   :align: right

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   cloudformation/find_new.rst
   cloudformation/send_email.rst
   cloudformation/scheduler.rst
   cloudformation/setup_db.rst

   cloudformation/rds.rst

   cloudformation/kms_key.rst

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
