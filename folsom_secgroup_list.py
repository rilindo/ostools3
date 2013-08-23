#!/usr/bin/env python

from ostools import *
import sys,getopt

openstack = OSTools('ostools.cfg')

# Display script usage
def usage():
    print("Usage: %s [ -u <UUID> | -i <INSTANCE> | -p <PRIVATE_IP> | -f <FLOATING_IP> ]" % sys.argv[0])
    print("      -u   UUID of instance")
    print("      -i   INSTANCE name [XXXXXXXX, i-XXXXXXXX, instance-XXXXXXXX]")
    print("      -p   Private IP Address of instance")
    print("      -f   Floating IP Address of instance")
    sys.exit(2)

########################
# Parse CLI options
########################
try:
    opts,args = getopt.getopt(sys.argv[1:],"u:i:p:f:")
except getopt.GetoptError:
    usage()

if not opts:
    usage()

########################
# Pull in VM info based on CLI args
########################
for opt, arg in opts:
    if opt in "-u":      # UUID
        try:
            user_id,created_at,instid,project_id,vm_state,hostname,host,uuid = openstack.vm_info('uuid',arg)
        except:
            print("Invalid uuid! [%s%s%s]" % (red,arg,nrm))
            sys.exit(2)
    elif opt in "-i":    # INSTANCE ID
        if "instance-" in arg or "i-" in arg:
            hexval = arg[arg.index('-')+1:] # Strip off "instance-" or "i-"
        else:
            hexval = arg
        try:
            instid = int(hexval,16)             # convert hex to dec
        except:
            print("Invalid instance name! [%s%s%s]" % (red,arg,nrm))
            sys.exit(2)
        try:
            user_id,created_at,instid,project_id,vm_state,hostname,host,uuid = openstack.vm_info('instance',instid)
        except:
            print("Invalid instance name! [%s%s%s]" % (red,arg,nrm))
            sys.exit(2)
    elif opt in "-p":
        uuid = openstack.uuid_by_fixedip(arg)
        if uuid:
            user_id,created_at,instid,project_id,vm_state,hostname,host,uuid = openstack.vm_info('uuid',uuid)
        else:
            print("Unable to locate instance!")
            sys.exit(2)
    elif opt in "-f":
        uuid = openstack.uuid_by_floatingip(arg)
        if uuid:
            user_id,created_at,instid,project_id,vm_state,hostname,host,uuid = openstack.vm_info('uuid',uuid)
        else:
            print("Unable to locate instance!")
            sys.exit(2)
    else:
        usage()

# Get list of security group id's for this host
grpidlist = openstack.secgrpid_list(uuid)

########################
# Output
########################
print("%sSecurity Groups for %s%s" % (uln,hostname,nrm))
if not grpidlist:
    print(" %sNONE%s" % (red,nrm))
for row in grpidlist: # Loop thru the groupid's assigned to this instance
    group = row[0]

    # Get the name & rules for this groupid
    groupname = openstack.secgrp_name(group)
    rules = openstack.secgrp_rule_list(group)

    print("%s%s (%s)%s" % (bld,groupname,group,nrm))
    if rules:
        for rule in rules:
            prot,fport,tport,cidr = rule
            print("    %-6s %-7s %-7s %-20s" % (prot,fport,tport,cidr))
    else:
        print("    %sNo rules!%s" % (red,nrm))
