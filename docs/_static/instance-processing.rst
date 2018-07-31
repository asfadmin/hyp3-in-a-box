.. _instance_processing:

AWS EC2 Processing Code
=======================

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   processing/hyp3_daemon.rst

Overview
--------

The HyP3 code that runs on EC2 instances is made up of 2 main components, the
"orchestration code" and the "science code". The orchestration code interfaces
with HyP3 infrastructure doing whatever setup is necessary. At some point it
will call the science code to do the actual processing needed to generate an
image. The orchestration code is always the same, regardless of the process
which is being run.

Orchestration Code
------------------

The part of the code which connects the science processing code to the rest of
the HyP3 infrastructure. It is responsible for the following tasks:

  * Checking SQS for new jobs
  * Parsing job info
  * Downloading Granule and DEM data
  * Running the science code
  * Uploading generated products
  * Notifying HyP3 of new the new products

Science Code
------------

This can be pretty anything as long as it provides a compatible interface. The
interface has yet to be determined, and will be outlined here.
