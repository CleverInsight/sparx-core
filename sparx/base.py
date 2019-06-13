"""
`Sparx Lite Server`
Author: @bastinrobin
"""
import tornado.ioloop
import tornado.web
from core import routes
from config import SETTINGS
from controllers.DocController import DocController

class Application(tornado.web.Application):
    ''' Application Route Declaration '''
    def __init__(self):
        handlers = routes()
        handlers.append((r'/docs', DocController))
        tornado.web.Application.__init__(self, handlers, **SETTINGS)
