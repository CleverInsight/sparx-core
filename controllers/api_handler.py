import os
import tornado.web
from base_handler import base_handler


class api_handler(base_handler):

    def get(self):
        ''' start the basic API seletion '''
        self.write("Welcome API world");