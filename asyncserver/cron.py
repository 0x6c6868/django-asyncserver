import gevent


def cron_func(seconds, func, *args, **kwargs):
    while True:
        gevent.sleep(seconds)
        func(*args, **kwargs)
