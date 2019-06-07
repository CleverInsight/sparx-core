import os
import sys
import yaml
import fileinput
from shutil import copyfile


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


def remove_service_files(controller_name):
    ''' Remove controller.py and .py* files '''

    if os.path.exists('controllers/' + controller_name + '.py'):
        os.remove('controllers/'+ controller_name + '.py')
    
    if os.path.exists('controllers/' + controller_name + '.pyc'):
        os.remove('controllers/'+ controller_name + '.pyc')


def remove_service(controller_name):
    ''' Remove the service added to the application '''

    # Modify yaml
    remove_from_yaml('routes.yml', controller_name)

    # Remove controller files
    remove_service_files(controller_name)

    # Remove declaration of import from __init__.py
    remove_declaration(controller_name)


if __name__ == "__main__":

    if sys.argv[1] == 'add':
        add_service(sys.argv[2], sys.argv[3])
    
    elif sys.argv[1] == 'rm':
        remove_service(sys.argv[2])

    else:
        print "Invalid commands"