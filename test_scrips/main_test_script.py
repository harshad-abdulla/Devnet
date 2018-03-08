from all_path import *
from base_lib import *
import os


###### Settings up all project directories ##############
directories = ['common_library', 'ospf_library', 'base_library', 'resources']

project_dirs = get_project_dir(directories)

set_sys_path(project_dirs)


###### Create log file name with timestamp+filename ##############
testcase = "DR_BDR_Test"
filename = "log_" + testcase + ".log"
logger = logging_file(filename)


#### Start of Test case ###########################
log_print("Starting Test case %s" % testcase, 1)


###############Step 1: Open session with DUT, Route R1 and Router R2 ###########
devices = get_devices("..\\resources\\devices.yaml")
log_print('DEVICE DETAILS')
log_print(str(devices))

flag = get_handle(devices)

for device in devices:
    log_print(device['message'] + device['ip'])

if not flag:
    log_print("Test Case Failed", 1)
