import os
import tornado.web
from base_handler import base_handler



class controller_name(base_handler):

    def get(self):
        ''' start the basic API seletion '''
        self.write();

    
    def post(self):
        ''' Create resources '''
        pass


    def put(self):
        ''' Update resources '''
        pass


    def delete(self):
        ''' Delete resources '''
        pass
    