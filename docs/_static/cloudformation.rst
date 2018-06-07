.. hyp3_api_eb.py  hyp3_find_new.py  hyp3_rds.py  hyp3_send_email.py  hyp3_vpc.py

.. _cloudformation:

AWS Cloudformation
==================


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   cloudformation/find_new.rst

Troposphere
-----------

`Troposphere`_ is a python library for generating cloudformation templates.
It is used as a lightweight wrapper around cloudformation to allow for
more dynamic environment then writing plain JSON provides

.. _Troposphere: https://github.com/cloudtools/troposphere

Template Generation
-------------------

The ``create_stack.py`` script is used to generate the raw cloudformaiton json.
It takes command line arguments of what resources should be included in the
template.

.. code-block:: bash

   python create_stack.py --find_new --api_eb outputs/template.json

This command makes a template with the :ref:`find_new_lambda` lambda and the elastic beanstalk
application that runs the API.

Troposphere Templates
---------------------

Each file in ``cloudformation/tropo/templates`` directory is responsible for creating a
logical portion of the Hy3P-In-A-Box infrastructure. Each flag in the ``create_stack.py``
corresponds to one of these file.
