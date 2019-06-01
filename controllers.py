'''
`Sparx Lite Server`
@module: Handlers
'''
import os
import sys
import tornado
import tornado.web
from lite import T
from version import version

__TEMPLATES__ = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/')



class BaseHandler(tornado.web.RequestHandler):
    '''
    @brief BaseHandler with all Mixin Configuration
    '''
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request)
        self.snippet = T

    def write_error(self, status_code, **kwargs):

        if status_code == 404:
            self.render('_includes/404.html', page=None, error=kwargs['exc_info'])
        elif status_code == 500:
            print kwargs
            self.render('_includes/500.html', page=None, error=kwargs['exc_info'])
        else:
            self.render('_includes/unknown.html', page=None)


    def set_default_headers(self):
        self.set_header('Server', 'Sparx-lite/' + '.'.join(str(v) for v in version))
        self.set_header('Organization', 'CleverInsight Labs')
        self.set_header('Author', 'Bastin Robins J')
        self.set_header("access-control-allow-origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, PUT, DELETE, OPTIONS')
        self.set_header("Access-Control-Allow-Headers", \
            "access-control-allow-origin,authorization,content-type")


    def get_current_user(self):
        return self.get_secure_cookie("user")

    def get_current_role(self):
        return self.get_secure_cookie("role")

    def get_current_email(self):
        return self.get_secure_cookie("email")


# Basic LimusBi server initialization
class MainHandler(BaseHandler):
    '''
    First inherited handler to load home template
    '''
    def get(self):
        self.render('index.html', handler=self, snippet=self.snippet, result=None)


class LoginHandler(BaseHandler):

    def check_permission(self, password, username):
        if username == "bastinrobin" and password == "demo.123":
            return True
        return False

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")

    def get(self):
        self.render('login.html')

    def post(self):

        username = self.get_argument('username')
        password = self.get_argument('password')

        auth = self.check_permission(password, username)

        if auth:
            self.set_current_user(username)
            self.redirect('/')
        else:
            self.write('You are not allowed to access this page')

class LogoutHandler(BaseHandler):
    '''
        `LogoutHandler` For the complete application
    '''
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))


class DocsHandler(BaseHandler):
    '''
        `DocsHandler` complete documentation rendering class
    '''
    def get(self):
        self.render('_includes/docs.html', snippet=self.snippet)


class TemplateHandler(BaseHandler):
    '''
        Global .html file handler
    '''
    def get(self, filename):
        raise tornado.web.HTTPError(status_code=404, log_message="template is not found")

    
__all__ = [
    MainHandler,
    LoginHandler,
    LogoutHandler,
    DocsHandler,
    BaseHandler,
    TemplateHandler
]
