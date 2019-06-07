import os
import tornado.web
from base_handler import base_handler



class IndexController(base_handler):

    def get(self):
        ''' start the basic API seletion '''
        self.render('welcome.html')

    
    def post(self):
        ''' Create resources '''
        pass


    def put(self):
        ''' Update resources '''
        pass


    def delete(self):
        ''' Delete resources '''
        pass
    