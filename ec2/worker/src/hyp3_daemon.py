#!/usr/bin/env python3.6
"""
Entry point for :ref:`hyp3_process`. This file is called from ``hyp3.service``
systemd startup script
"""

import hyp3_handler
from hyp3_process import Process


def main():
    """ Run a new process with the handler function imported from
    ``hyp3_handler.py``.
    """
    process = Process(
        handler_function=hyp3_handler.handler
    )
    process.run()


if __name__ == '__main__':
    main()
