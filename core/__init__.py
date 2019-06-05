import os
import sys
import yaml
import types
import yamlordereddictloader
from controllers import *




def str_to_class(classname):
    ''' Take a `classname` and convert to python `Class` '''
    try:
        identifier = getattr(sys.modules[__name__], classname)
    except AttributeError:
        raise NameError("%s doesn't exist." % classname)
    if isinstance(identifier, (types.ClassType, types.TypeType)):
        return identifier
    raise TypeError("%s is not a class." % classname)

    

def read_yaml(filename):
    ''' take filename as parameter and convert yaml to ordereddict '''
    return yaml.load(open(filename))



def make_route_tuple(data):
    response = []

    for v in zip(data['url'], data['controllers']):
        url, controller = v
        response.append((url, str_to_class(controller)))
    return response


def routes():
    ''' for routes data from routes.yml file '''
    yaml_file = os.path.join(os.path.abspath(os.curdir), 'routes.yml')
    routes = read_yaml(yaml_file)
    
    return make_route_tuple(routes)
