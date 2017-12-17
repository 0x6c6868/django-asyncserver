from django.core.servers.basehttp import get_internal_wsgi_application
from django.core.management.base import BaseCommand, CommandError
from django.utils import module_loading
from django.utils import autoreload
from django.conf import settings

from django.contrib.staticfiles.handlers import StaticFilesHandler

import gevent
from gevent.wsgi import WSGIServer

from ...cron import cron_func
from ...config import KNOWN_SETTINGS


class Command(BaseCommand):
    help = 'An asyncserver for Django base on gevent.'

    @property
    def addr(self):
        return self.options["host"]

    @property
    def port(self):
        return self.options["port"]

    def get_handler(self):
        return StaticFilesHandler(get_internal_wsgi_application())

    def add_arguments(self, parser):
        for setting in KNOWN_SETTINGS:
            kwargs = {key: getattr(setting, key) for key in setting.__dict__ if not key.startswith("_")}
            parser.add_argument(getattr(setting, "_name"), **kwargs)

    def handle(self, *args, **options):
        if not settings.DEBUG and not settings.ALLOWED_HOSTS:
            raise CommandError('You must set settings.ALLOWED_HOSTS if DEBUG is False.')

        self.options = options
        self.run(**options)

    def run(self, **options):
        is_debug = getattr(settings, "DEBUG", True)
        if is_debug:
            autoreload.main(self.inner_run, None, options)
        else:
            self.inner_run(**options)

    def inner_run(self, **options):
        # run cron jobs
        cron_jobs = getattr(settings, "ASYNC_SERVER_CRON_JOBS", [])
        for job in cron_jobs:
            secs = job.get("secs", 0)
            func = job.get("func", "")

            if not secs or not func:
                raise CommandError("secs or func can not be null.")

            self.stdout.write("cron job %s is running" % func)

            func = module_loading.import_string(func)
            gevent.spawn(cron_func, secs, func)

        app = self.get_handler()
        server = WSGIServer((self.addr, int(self.port)), app)

        self.stdout.write((
              "django asyncserver is running at http://%(addr)s:%(port)s"
        ) % {
            "addr": self.addr,
            "port": self.port,
        })

        server.serve_forever()
