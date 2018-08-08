from hyp3_process import Process

import hyp3_handler


def run():
    process = Process(
        handler_function=hyp3_handler.handler
    )

    start_worker(process)


def start_worker(process):
    process.run()
