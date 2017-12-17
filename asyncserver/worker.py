import gevent
from gevent.queue import Queue


class Worker(object):
    pass


class SyncWorker(Worker):

    @staticmethod
    def run(spawns):
        jobs = []
        for spawn in spawns:
            func = spawn.get("func", None)
            args = spawn.get("args", [])
            kwargs = spawn.get("kwargs", {})

            jobs.append(gevent.spawn(func, *args, **kwargs))

        gevent.joinall(jobs)
        return [job.get() for job in jobs]


class AsyncWorker(Worker):
    def __init__(self, worker_nums=5):
        self._queue = Queue()

        for _ in range(worker_nums):
            gevent.spawn(self._start_workers)

    def _start_workers(self):
        while True:
            func, args, kwargs = self._queue.get()
            func(*args, **kwargs)

    def run(self, func, *args, **kwargs):
        self._queue.put_nowait((func, args, kwargs))
