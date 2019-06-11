import os
import json
import tornado.web
from base_handler import base_handler



class controller_name(base_handler):

    def get(self):
        ''' start the basic API seletion '''
        data = dict(
            source='controllers/{}'.format('controller_name.py'),
            response=[]
        )
        self.write(json.dumps(data))
        self.finish()

    
    def post(self):
        ''' Create resources '''
        pass


    def put(self):
        ''' Update resources '''
        pass


    def delete(self):
        ''' Delete resources '''
        pass
    