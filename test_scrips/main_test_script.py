from all_path import *
from base_lib import *

directories = ['common_library', 'ospf_library', 'base_library', 'resources']

project_dirs = get_project_dir(directories)

set_sys_path(project_dirs)

devices = get_devices("..\\resources\\devices.yaml")
print devices
