#!/usr/bin/env python

from ostools import *
import sys,getopt

openstack = OSTools('ostools.cfg')
got_fixed_ip = True

def usage():
    print("Usage: %s [ -u <UUID> | -i <INSTANCE> | -p <PRIVATE_IP> | -f <FLOATING_IP> ]" % sys.argv[0])
    print("      -u   UUID of instance")
    print("      -i   INSTANCE name [XXXXXXXX, i-XXXXXXXX, instance-XXXXXXXX]")
    print("      -p   Private IP Address of instance")
    print("      -f   Floating IP Address of instance")
    sys.exit(2)


#########################
# Parse CLI options
#########################
try:
    opts,args = getopt.getopt(sys.argv[1:],"u:i:p:f:")
except getopt.GetoptError:
    usage()

if not opts:
    usage()

for opt, arg in opts:
    if opt in "-u":
        uuid = arg
    elif opt in "-i":
        if "instance-" in arg or "i-" in arg:
            hexval = arg[arg.index('-')+1:] # Strip off "instance-" or "i-"
        else:
            hexval = arg
        try:
            instid = int(hexval,16)             # convert hex to dec
        except:
            print("Invalid instance name! [%s%s%s]" % (red,arg,nrm))
            sys.exit(2)
        uuid = openstack.uuid_by_instanceid(instid)
    elif opt in "-p":
        uuid = openstack.uuid_by_fixedip(arg)
    elif opt in "-f":
        uuid = openstack.uuid_by_floatingip(arg)
    else:
        usage()

if not uuid:
    print("Unable to locate instance!")
    sys.exit(2)

#########################
# Gather all the data
#########################
try:
    user_id,created_at,instid,project_id,vm_state,hostname,host,uuid = openstack.vm_info('uuid',uuid)
except:
    print("Invalid uuid! [%s%s%s]" % (red,uuid,nrm))
    sys.exit(2)
volumes = openstack.volumes_by_uuid(uuid)
user_info = openstack.user_info_by_id(user_id)
user_name = user_info[0]

# Sometimes an instance doesn't have a fixed_ip (not good!)
try:
    fixedip = openstack.fixedip_by_uuid(uuid)
except:
    got_fixed_ip = False
    fixedip = "%sNo fixed_ip for instance!%s" % (red, nrm)
if got_fixed_ip:
    fixedipid = openstack.fixedipid_by_uuid(uuid)
    floating_ips = openstack.floatingips_by_fixedipid(fixedipid)
else:
    floating_ips = None

# There can be orphaned instances w/o a tenant in Keystone
try:
    tenant_name = openstack.tenant_name(project_id)
except:
    tenant_name = "%sNo Keystone record for tenant!%s" % (red, nrm)

#########################
# OUTPUT
#########################
print
print("Hostname: %s" % hostname)
print(" Created: %s" % created_at)
print(" Creator: %s [%s]" % (user_id, user_name))
print("    UUID: %s" % uuid)
print("Instance: instance-%08x" % instid)
print("TenantID: %s" % project_id)
print("  Tenant: %s" % tenant_name)
print(" Compute: %s" % host)
print("   State: %s" % vm_state)
print("   Fixed: %s" % fixedip)
if floating_ips:
    for x in floating_ips:
        print("Floating: %s" % x)
if volumes:
    print(" Volumes:")
    for vol in volumes:
        print("          %s [%s]" % (vol[1], vol[8]))
print
