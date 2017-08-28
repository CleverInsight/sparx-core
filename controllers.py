from version import version
import tornado
import pulp
import sys
import pandas as pd
from lite import T


class BaseHandler(tornado.web.RequestHandler):

    def __init__(self,application, request,**kwargs):
            super(BaseHandler,self).__init__(application,request)
            self.snippet = T

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('_includes/404.html',page=None, error=kwargs['exc_info'])
        elif status_code == 500:
            print kwargs
            self.render('_includes/500.html',page=None, error=kwargs['exc_info'])
        else:
            self.render('_includes/unknown.html',page=None)

    def set_default_headers(self):
        self.set_header('Server', 'Sparx-lite/' + '.'.join(str(v) for v in version))
        self.set_header('Company', 'CleverInsight Labs')
        self.set_header('Author', 'Bastin Robins J')

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def get_current_role(self):
        return self.get_secure_cookie("role")

    def get_current_email(self):
        return self.get_secure_cookie("email")



# Basic LimusBi server initialization
class MainHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        self.render('index.html', handler=self, snippet=self.snippet, result=None)


    def post(self):

        # Problem data
        idx = [0, 1, 2, 3, 4]
        d = {'Dept': pd.Series(['Receiving', 'Picking', 'PPicking', 'QC', 'Packing'], index=idx),
             'Target': pd.Series([61, 94, 32, 63, 116], index=idx),
             'Hrs/day': pd.Series([7.75, 7.75, 7.75, 7.75, 7.75], index=idx),
             'Prod': pd.Series([int(self.get_argument('receiving')), int(self.get_argument('picking')), int(self.get_argument('ppicking')), int(self.get_argument('qc')), int(self.get_argument('packing'))], index=idx)}
        df = pd.DataFrame(d)

        # Create variables and model                                                                                                 
        HC = pulp.LpVariable.dicts("HC", df.index, lowBound=0)
        OT = pulp.LpVariable.dicts("OT", df.index, lowBound=0)
        mod = pulp.LpProblem("OTReduction", pulp.LpMinimize)

        # # # Objective function                                                                                                         
        mod += sum([OT[idx] for idx in df.index])

        # # Lower and upper bounds:                                                                                                    
        for idx in df.index:
            mod += df['Target'][idx] * df['Hrs/day'][idx] * HC[idx] + df['Target'][idx] * OT[idx] >= df['Prod'][idx]

        # Total HC value should be less than or equal to 92                                                                          
        mod += sum([HC[idx] for idx in df.index]) <= int(self.get_argument('hc'))


        # Solve model                                                                                                                
        mod.solve()

        # Output solution   
        hc, ot = [], []                                                                                                    
        for idx in df.index:
            hc.append(int(HC[idx].value()))
            ot.append(OT[idx].value())
        df['HC'] = pd.Series(hc)
        df['OT'] = pd.Series(ot)

        self.render('index.html', handler=self, snippet=self.snippet, \
            result=df[['Dept', 'HC', 'OT']].to_html(classes='table table-bordered'), OT=df['OT'].sum(), HC=df['HC'].sum())

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
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))

class DocsHandler(BaseHandler):

    def get(self):
        self.render('_includes/docs.html', snippet=self.snippet)