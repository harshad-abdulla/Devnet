from automate import *
import time


devices = get_devices("devices.yaml")
print devices


handle = get_handle(devices)

# print devices

print "Fetching raw data..."
data = get_ospf_neighbours(devices[0]['handle'])
print data

print "Fetching DR/BDR...."
# result = get_dr_bdr(devices[0]['handle'])

# finds the DR and BDR
for device in devices:
    print get_ospf_neighbours(device['handle'])
    dr, bdr = get_dr_bdr(device['handle'])
    if dr == 0 or bdr == 0:
        continue
        dr, bdr = get_dr_bdr(device['handle'])
    else:
        break

print 'DR: ' + str(dr)
print "BDR: " + str(bdr)

# Disable ospf in the current DR
for device in devices:
    if device['ip'] == dr:
        print 'Disabling ospf on ' + dr
        print disable_ospf(device['handle'], '1')
    else:
        continue

print "Waiting for OSPF to load to FULL State"
time.sleep(40)

# Find the new DR and BDR
print "Finding new DR and BDR...."
for device in devices:
    print get_ospf_neighbours(device['handle'])
    new_dr, new_bdr = get_dr_bdr(device['handle'])
    if new_dr == 0:
        continue
        new_dr, new_bdr = get_dr_bdr(device['handle'])
    else:
        break

print 'New DR:' + str(new_dr)
print 'New BDR:' + str(new_bdr)

if bdr == new_dr and new_dr != 0:
    print '--------------TEST SUCCESS--------------------'
else:
    print '--------------TEST FAILED--------------------'
