from netmiko import ConnectHandler
from yaml import load
import time
import os
import logging
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException


def logging_file(filename):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    date1 = time.strftime("%Y%m%d")

    log_dir = os.path.abspath('..\logs')
    log_dir_with_date = os.path.join(log_dir, date1)

    if not os.path.exists(log_dir_with_date):
        os.makedirs(log_dir_with_date)

    log_file_name = log_dir_with_date + '\\' + timestr + filename
    logger = logging.getLogger('mytest')
    hdlr = logging.FileHandler(log_file_name)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    logger.info('from logging_file function')
    return logger


def log_print(string, highlight=0):
    highlighter = '#' * 50
    logger = logging.getLogger('mytest')
    if highlight:
        print highlighter
        logger.info(highlighter)
    print string
    for x in string.split('\n'):
        logger.info(x)
    if highlight:
        print highlighter
        logger.info(highlighter)


def get_devices(file_name):
    """Read the device data from the device json file and return it as a dictionary"""
    with open(file_name, 'r') as f:
        dump = load(f)
    n = int(dump['Device_count'])
    devices = []
    while (n > 0):
        devices.append(dump['Device_' + str(n)])
        n = n - 1
    return devices


def get_handle(devices):
    """Takes a list of device dictionsary and embeds the connection handle with the dictionary"""
    msg = ''
    flag = 1
    for device in devices:
        ip = device['ip']
        try:
            handle = ConnectHandler(**device)
            msg = 'Connected to: '
        except (AuthenticationException):
            msg = 'Authentication failure: '
            flag = 0
        except (NetMikoTimeoutException):
            msg = 'Timeout of Device: '
            flag = 0
        except (EOFError):
            msg = 'End of file attempting to device: '
            flag = 0
        except (SSHException):
            msg = 'SSH issue! Make you sure SSH is enabled on:'
            flag = 0
        except Exception as unknown_error:
            msg = 'Error Occurred: ' + str(unknown_error)
            flag = 0

        device['handle'] = handle
        device['message'] = msg
    return flag
