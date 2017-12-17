import requests
from django.http import HttpResponse
from asyncserver.worker import SyncWorker

from .async_job import do_async_job


def async_test(request):
    do_async_job(delay=2)
    return HttpResponse("async_test")


def sync_test(request):
    result = SyncWorker.run([
        {"func": requests.get, "args": ["http://www.baidu.com"], "kwargs": {}},
        {"func": requests.get, "args": ["http://www.taobao.com"], "kwargs": {}},
        {"func": requests.get, "args": ["http://www.alibaba.com"], "kwargs": {}},
        {"func": requests.get, "args": ["http://www.qq.com"], "kwargs": {}},
    ])
    result = map(lambda r: "crawl " + r.url + " success", result)
    result = "<br>".join(result)
    return HttpResponse(result)
