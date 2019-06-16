import os
import sys
import yaml
import argparse
import tornado
import logging
import fileinput
from shutil import copyfile
from prettytable import PrettyTable
from base import Application
from tornado.options import options
from version import version


__UPLOADS__  = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources/')
__MODELS__  = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources/models/')
# __STORAGE__ = 


# Argument parser
parser = argparse.ArgumentParser(description="Sparx Application Command Line")
parser.add_argument('service', help="Type of service command")
parser.add_argument('-t', '--type', type=str, metavar='', help='Type of command add or rm')
parser.add_argument('-u', '--url', type=str, metavar='', help='API endpoints url')
parser.add_argument('-c', '--controller', type=str, metavar='', help='Endpoint controller')
parser.add_argument('-m', '--model', type=str, metavar='', help='Pickled predictive model `*.pkl` ')
args = parser.parse_args()



def line_prepender(filename, line):
    ''' Add new line to give file first line '''
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)


def read_yaml(filename):
    ''' take filename as parameter and convert yaml to ordereddict '''
    return yaml.load(open(filename))


def add_to_yaml(filename, route, controller_name):
    ''' Read `routes.yaml` file and replace the given variables '''
    data = read_yaml(filename)
    data['urls'].append(route)
    data['controllers'].append(controller_name)

    with open(filename, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)



def remove_from_yaml(filename, controller_name):
    ''' Remove the given controller entry from yaml '''
    data = read_yaml(filename)
    urls, controllers = [], []
    for url, controller in zip(data['urls'], data['controllers']):
        if controller != controller_name:
            urls.append(url)
            controllers.append(controller)
    
    data['urls'], data['controllers'] = urls, controllers

    with open(filename, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)




def clone_script(origin_script, controller_name):
    '''
    Copy the controller skeleton and clone it into 
        controllers directory with name change
    '''
    dest_location = 'controllers/' + controller_name + '.py'

    with open(origin_script, 'r') as f:
        new_content = f.read().replace('controller_name', controller_name)
        f.close()
    
    with open(dest_location, "w") as f:
        f.write(new_content)



def clone_model(src, controller_name, destination="resources/models"):
    ''' Copy trained model from local to model repository '''
    destination = os.path.join(destination, controller_name + '.pkl')
    copyfile(src, destination)
    print "Model imported successfully..."



def remove_declaration(controller_name):
    ''' `TODO` Scan and remove the controller declaration and save the file '''

    main_location = 'controllers/__init__.py'

    declaration = 'from ' + controller_name + ' import *'
    with open(main_location, "r") as f:
        lines = f.readlines()
    with open(main_location, "w") as f:
        for line in lines:
            if line.strip("\n") != declaration:
                f.write(line)


def add_service(url, controller_name):
    add_to_yaml('routes.yml', url, controller_name)
    clone_script('core/skeleton/controller.py', controller_name)
    line_prepender('controllers/__init__.py', 'from ' + str(controller_name) + ' import *')
    print "new service generated ..."


def add_ml_service(url, controller_name, model_file):
    ''' Add ML/DL pickled model service '''
    add_to_yaml('routes.yml', url, controller_name)
    clone_script('core/skeleton/model_controller.py', controller_name)
    clone_model(model_file, controller_name)
    line_prepender('controllers/__init__.py', 'from ' + str(controller_name) + ' import *')
    print "new machine learning service generated ..."




def remove_service_files(controller_name):
    ''' Remove controller.py and .py* files '''

    if os.path.exists('controllers/' + controller_name + '.py'):
        os.remove('controllers/'+ controller_name + '.py')
    
    if os.path.exists('controllers/' + controller_name + '.pyc'):
        os.remove('controllers/'+ controller_name + '.pyc')

    if os.path.exists('resources/models/' + controller_name + '.pkl'):
        os.remove('resources/models/' + controller_name + '.pkl')


def remove_service(controller_name):
    ''' Remove the service added to the application '''

    if controller_name == 'IndexController':
        sys.exit('Error: IndexController cannot be removed!')

    # Modify yaml
    remove_from_yaml('routes.yml', controller_name)

    # Remove controller files
    remove_service_files(controller_name)

    # Remove declaration of import from __init__.py
    remove_declaration(controller_name)

    print "Removed {}".format(controller_name)



def list_all_endpoints():
    '''
    List all apps created inside give directory
    '''

    apps = read_yaml('routes.yml')

    table = PrettyTable(['Routes', 'Controllers'])
    for url, controller in zip(apps['urls'], apps['controllers']):
        table.add_row([url, controller])
    table.align = 'l'
    print table

    
def start_app():
    ''' Sparx server instantiation'''

    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    logging.info('*** Sparx-core - version '+ str(version) +'. started at:\
     http://localhost:%d/' % (options.port))
    tornado.ioloop.IOLoop.instance().start()



if __name__ == "__main__":
    
    # Check if `add` service command
    if args.service == 'add':
        if args.url != None and args.controller != None:

            # check if model flag is defined
            if args.model == None:

                # create a normal service if model is `None`
                add_service(args.url, args.controller)

            else:
                # check if give model file exists
                if os.path.exists(args.model):

                    # Add ml service if model is defined
                    add_ml_service(args.url, args.controller, args.model)
                
                else:
                    # throw exception
                    print 'Model path not defined'

        else:

            # Throw -u and -c required exception
            print "`-u` URL required"
            print "`-c` Controller required"


    # Check if `rm` (remove) command
    elif args.service == 'rm':
        if args.controller != None:
            remove_service(args.controller)
        else:
            print "controller name is required `-c`"

    # List all service from routes.yml
    elif args.service == 'endpoints':
        list_all_endpoints()
    
    # Start the sparx-core server
    elif args.service == 'start':
        start_app()

    else:
        print "Invalid commands"
