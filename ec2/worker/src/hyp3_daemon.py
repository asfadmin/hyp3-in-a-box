#!/usr/local/bin/python3.6

from hyp3_process import Process

import hyp3_handler


if __name__ == '__main__':
    process = Process(
        handler_function=hyp3_handler.handler
    )
    process.run()
