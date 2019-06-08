"""
`Sparx Lite Server`
Author: @bastinrobin
"""
import tornado.ioloop
import tornado.web
from core import routes
from config import SETTINGS

class Application(tornado.web.Application):
    ''' Application Route Declaration '''
    def __init__(self):
        tornado.web.Application.__init__(self, routes(), **SETTINGS)
