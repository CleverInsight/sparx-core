import os
import yaml
import json
import tornado.web
from base_handler import base_handler


_conf = yaml.load(open('controllers/ApiController.yml'))

class ApiController(base_handler):

    def get(self):
        ''' start the basic API seletion '''

        data = dict(
            source='controllers/{}'.format('ApiController.py'),
            response=[]
        )
        self.write(json.dumps(_conf['get']['response']))
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
    