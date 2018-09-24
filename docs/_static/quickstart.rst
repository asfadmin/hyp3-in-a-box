.. _quickstart:

API Quickstart
==============

Creating A Subscription
~~~~~~~~~~~~~~~~~~~~~~~

    To start processing data, a subscription needs to be created.

        * Select your created hyp3-in-a-box cloudformation stack
        * URL for the HyP3 API is in the stack outputs.
        * Navigate to the HyP3 API website
        * Click on ``create_subscription`` and fill out the subscription form.

    An example subscription will look something like this:

    .. image:: ../_static/images/example-subscription.png
       :alt: alternate text
       :align: right

    Change the ``location`` parameter to be a valid WKT Multipolygon over your area of intrest. Example:

    .. code-block:: python

       MULTIPOLYGON (((40 40, 20 45, 45 30, 40 40)))

    Possible process_id's can be found py running a get_processes API call. The ``Username`` and ``API Key``
    can also be found as stack outputs, where the API URL was found. If the stack has been updated,
    these parameters will be in **Systems Manager: Parameter Store** instead. The Parameter Store Names
    for these parameter will be in the stack outputs.

    **Note:** Currently ``platform`` and ``crop_to_selection`` are not implimented, so they have no effect.
    They must still be entered because of the API parameter validation.

