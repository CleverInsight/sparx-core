import os
from tornado.template import Template

__SNIPPET__ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_snippet')


def T(name, **kw):
	t = Template(open(os.path.join(__SNIPPET__, name + '.html'), 'rb').read())
	return t.generate(**dict([('template_file', name)] + globals().items() + kw.items()))
