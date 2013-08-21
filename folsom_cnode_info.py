#!/usr/bin/env python

from ostools import *
import os,sys,getopt

openstack = OSTools('ostools.cfg')
quiet = False
sort = ''

def usage():
    print("Usage: %s " % sys.argv[0])
    print("      -r   Reverse sort order")
    print("      -q   Suppress header")
    print("      -h   This help")
    sys.exit(2)

#########################
# Parse CLI options
#########################
try:
    opts,args = getopt.getopt(sys.argv[1:],"hrq")
except getopt.GetoptError:
    usage()

for opt, arg in opts:
    if opt in "-h":
        usage()
        sys.exit(0)
    elif opt in "-r":
        sort = 'DESC'
    elif opt in "-q":
        quiet = True
    else:
        usage()

#########################
# OUTPUT
#########################
cnodes = openstack.cnode_info(sort)
if not quiet:
    print("%s%s%-4s %-7s %-14s %-10s %s%s" % (bld,uln,"VMs","VCPU","RAM","STATUS","CNODE",nrm))
for cnode in cnodes:
    cpu = str(cnode['vcpus_used']) + '/' + str(cnode['vcpus'])
    ram = str(cnode['memory_mb_used']) + '/' + str(cnode['memory_mb'])
    host = cnode['hypervisor_hostname'].split('.')[0]
    if cnode['status']:
       state = "disabled"
    else:
       state = "enabled"
    print("%-4s %-7s %-14s %-10s %s" % (cnode['running_vms'],cpu,ram,state,host))
