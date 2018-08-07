from hyp3_process import Process

import hyp3_handler

process = Process()


def run():
    process.add_handler(hyp3_handler.handler)

    start_worker(process)


def start_worker(process):
    process.run()
