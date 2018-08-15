.. _instance_processing:

AWS EC2 Processing Code
=======================

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   processing/hyp3_daemon

Overview
--------

The HyP3 code that runs on EC2 instances is made up of 2 main components, the
"orchestration code" and the "science code". The orchestration code interfaces
with HyP3 infrastructure doing whatever setup is necessary. At some point it
will call the science code to do the actual processing needed to generate an
image. The orchestration code is always the same, regardless of the process
which is being run.

Science Code
------------

This can be pretty anything as long as it provides a compatible interface.
A python file called ``hyp3_handler.py`` containing a function called ``handler``

Orchestration Code
------------------

The part of the code which connects the science processing code to the rest of
the HyP3 infrastructure.

The ``hyp3_handler.py`` script is imported by the ``ec2/worker/hyp3_daemon.py`` script,
which is part of the orchestration code and is process agnostic. This script uses
the :ref:`hyp3_process` module to wrap processing functionality around the handler
function and then starts a daemon to pull new jobs from an SQS Queue, run processing and
push outputs to a SNS Topic.

