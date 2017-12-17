# DjangoAsyncServer

* cpython 3.6.4
* Django 2.0

## gevent monkey patch

``manage.py``
~~~python
from asyncserver import monkey
monkey.patch_all()
~~~

``settings.py``
~~~python
INSTALLED_APPS = [
    ...
    "asyncserver",
]
~~~

## cron jobs

``settings.py``
~~~python
ASYNC_SERVER_CRON_JOBS = [
    {"secs": 60, "func": "xxx.xxx.xxx.sync_data"},
]
~~~

## async worker
~~~python
def foo(bar):
    print("hello ", bar)

from asyncserver.worker import AsyncWorker
async_worker = AsyncWorker(worker_nums=10)
async_worker.run(foo, "world")
~~~

## sync worker
~~~python
import requests

from asyncserver.worker import SyncWorker

results = SyncWorker.run([
    {"func": requests.get, "args": ["http://www.baidu.com"], "kwargs": {}},
    {"func": requests.get, "args": ["http://www.taobao.com"], "kwargs": {}},
    {"func": requests.get, "args": ["http://www.alibaba.com"], "kwargs": {}},
    {"func": requests.get, "args": ["http://www.qq.com"], "kwargs": {}},
])
~~~
