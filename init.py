"""
Sparx Lite Server
Author: @bastinrobin
"""
import os
import logging
from version import version
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from controllers import *


define("port", default=5000, help="run on the given port", type=int)
define('nobrowser', default=True, help='Do not start webbrowser', type=bool)
SOURCE = os.path.dirname(os.path.abspath(__file__))


class Application(tornado.web.Application):
    ''' Application Route Declaration '''
    def __init__(self):

        handlers = [
            (r"/", MainHandler),
            (r"/docs", DocsHandler),
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler)
        ]
        settings = dict(
            cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            autoreload=True,
            gzip=True,
            debug=True,
            login_url='/login',
            autoescape=None
        )

        tornado.web.Application.__init__(self, handlers, **settings)


def start_app():
    ''' Sparx server instantiation'''
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    # if not options.nobrowser:
    #     try:
    #         import webbrowser
    #         webbrowser.open('http://127.0.0.1:%d' % options.port)
    #     except ImportError:
    #         pass
    # logging.info('*** Sparx-lite - version '+ str(version) +'. started at:\
    #  http://localhost:%d/' % (options.port))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    start_app()
