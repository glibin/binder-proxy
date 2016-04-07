#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
import logging.handlers

import tornado.ioloop
import tornado.web
import tornado.options
import tornado.locale
import tornado.httpserver
import tornado.httpclient
import tornado.netutil
import tornado.gen
from tornado.options import options
from tortik.logger import tortik_log, RequestIdFilter

import config
from handler import ProxyHandler


class Application(tornado.web.Application):
    def __init__(self):
        handlers = []

        static_path = options.static_path or os.path.join(os.path.dirname(__file__), 'static')
        js_static_path = os.path.join(static_path, 'js')
        css_static_path = os.path.join(static_path, 'css')

        handlers.extend([
            (r'/js/(.*)', tornado.web.StaticFileHandler, {'path': js_static_path}),
            (r'/css/(.*)', tornado.web.StaticFileHandler, {'path': css_static_path}),
            (r'.*', ProxyHandler),
        ])

        settings = dict(
            xsrf_cookies=False,
            static_path=static_path,
            debug=options.debug,
            autoescape=None
        )

        tornado.web.Application.__init__(self, handlers, **settings)

        configure_logging()


def configure_logging():
    tortik_log.addFilter(RequestIdFilter())
    tortik_log.setLevel(options.log_level)

    logger = logging.getLogger()
    logger.setLevel(options.log_level)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    tornado.options.parse_config_file(options.config)
    tornado.options.parse_command_line()

    tornado.httpclient.AsyncHTTPClient.configure('tornado.simple_httpclient.SimpleAsyncHTTPClient', max_clients=30)
    tornado.netutil.Resolver.configure(options.resolver)

    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port, options.host)

    logging.info('Starting server at http://{}:{}'.format(options.host, options.port))

    tornado.ioloop.IOLoop.instance().start()
