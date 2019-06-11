import os
import sys
import json
import tornado
import tornado.web

class base_handler(tornado.web.RequestHandler):
    '''
    @brief base_handler with all Mixin Configuration
    '''
    def __init__(self, application, request, **kwargs):
        super(base_handler, self).__init__(application, request)
    

    def write_error(self, status_code, **kwargs):
        ''' Error handling '''

        if status_code == 404:
            self.render('_includes/404.html', page=None, error=kwargs['exc_info'])
        elif status_code == 500:
            print kwargs
            self.render('_includes/500.html', page=None, error=kwargs['exc_info'])
        else:
            self.render('_includes/unknown.html', page=None)


    def set_default_headers(self):
        self.set_header('Server', 'Sparx-Core/')
        self.set_header('Organization', 'CleverInsight Labs')
        self.set_header('Author', 'Bastin Robins J')
        self.set_header('Co-Author', 'Dr.Vandana Bhagat')
        self.set_header("access-control-allow-origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, PUT, DELETE, OPTIONS')
        self.set_header("Access-Control-Allow-Headers", \
            "access-control-allow-origin,authorization,content-type")


    def get_current_user(self):
        ''' Set current `user` cookie '''
        return self.get_secure_cookie("user")

    def get_current_role(self):
        ''' Get current `User` roles '''
        return self.get_secure_cookie("role")

    def get_current_email(self):
        ''' Get current `User` email '''
        return self.get_secure_cookie("email")