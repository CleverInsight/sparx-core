import os
import sqlite3
from tornado.options import define

# Standard Config
define("port", default=5000, help="run on the given port", type=int)


SOURCE = os.path.dirname(os.path.abspath(__file__))

SETTINGS = dict(

    cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    xsrf_cookies=False,
    autoreload=True,
    gzip=True,
    debug=True,
    login_url='/login',
    autoescape=None
)

CONN = sqlite3.connect('data.db')


def _execute(query):
    """Function to execute queries against a local sqlite database"""
    cur = CONN.cursor()
    
    try:
        result = cur.execute(query)

    except sqlite3.OperationalError:
        pass

    conn.commit()
    return result