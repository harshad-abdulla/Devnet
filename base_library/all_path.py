import sys
import os
#import logging

# filename='Project.log'
#logging.basicConfig(format='%(asctime)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

project_path = os.path.abspath('..')


def get_project_dir(dirs):
    """Get the directory list and genrate the corresponding directory path"""
    for directory in dirs:
        yield os.path.join(project_path, directory)


def set_sys_path(dirs):
    """Gets the directory path and set to sys path"""
    for directory in dirs:
        if directory in sys.path:
            continue
        else:
            sys.path.append(directory)
