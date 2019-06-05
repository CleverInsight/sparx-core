"""
`Sparx Lite Server`
Author: @bastinrobin
"""
import sys
import os
import logging
from version import version
import tornado.ioloop
import tornado.web
from tornado.options import options
from core import routes
from config import SETTINGS




# Get list of all routes from `YAML`


# Get list of all respective controllers from `YAML`



class Application(tornado.web.Application):
    ''' Application Route Declaration '''
    def __init__(self):
        tornado.web.Application.__init__(self, routes(), **SETTINGS)




def start_app():
    ''' Sparx server instantiation'''
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    logging.info('*** Sparx-lite - version '+ str(version) +'. started at:\
     http://localhost:%d/' % (options.port))
    tornado.ioloop.IOLoop.instance().start()



if __name__ == "__main__":
    start_app()
