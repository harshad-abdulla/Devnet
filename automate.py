from netmiko import ConnectHandler
from yaml import load
import re
import time
import os
import logging
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException


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
    for device in devices:
        ip = device['ip']
        try:
            handle = ConnectHandler(**device)
        except (AuthenticationException):
            print 'Authentication failure: ' + ip
            continue
        except (NetMikoTimeoutException):
            print 'Timeout of Device: ' + ip
            continue
        except (EOFError):
            print 'End of file attempting to device: ' + ip
            continue
        except (SSHException):
            print 'SSH issue! Make you sure SSH is enabled on:' + ip
            continue
        except Exception as unknown_error:
            print 'Error Occurred: ' + str(unknown_error)
            continue

        device['handle'] = handle
    return 1


def set_ospf_network(handler, pid, network, mask, area):
    """Configure ospf for the router and returns the config commands"""
    config_commands = ["router ospf " + pid,
                       "network " + network + ' ' + mask + ' ' + "area " + area]
    output = handler.send_config_set(config_commands)
    return output


def get_ospf_neighbours(handler):
    """Returns the ospf neighbour"""
    output = handler.send_command('show ip ospf neighbor')
    return output


def get_dr_bdr(handler):
    """Gets the ospf neighbour data and finds the DR/BDR data"""
    data = get_ospf_neighbours(handler)

    dr_regex = re.compile(r'((FULL/DR)(\s*\d\d:\d\d:\d\d\s*)((((25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])\.){3})(25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])))')
    bdr_regex = re.compile(r'((FULL/BDR)(\s*\d\d:\d\d:\d\d\s*)((((25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])\.){3})(25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])))')

    dr_mo = dr_regex.search(data)
    bdr_mo = bdr_regex.search(data)

    if dr_mo is not None:
        dr = dr_mo.group(4)
    else:
        dr = 0

    if bdr_mo is not None:
        bdr = bdr_mo.group(4)
    else:
        bdr = 0

    return dr, bdr


def disable_ospf(handler, pid):
    output = handler.send_config_set(['no router ospf ' + pid])
    return output


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
