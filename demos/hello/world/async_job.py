import gevent

from asyncserver.worker import AsyncWorker

async_server = AsyncWorker(10)


def do_async_job(delay=0):
    def _run():
        if delay:
            gevent.sleep(delay)
        print("send mail 2 sec later")

    async_server.run(_run)
