#!/usr/bin/env python

from ostools import *
import sys,getopt

openstack = OSTools('ostools.cfg')
quiet = False

def usage():
    print("Usage: %s [ -c <CNODE> | -t <TENANT_ID> ] -q" % sys.argv[0])
    print("      -n   The hostname OR partial match (4 character minimum)")
    print("      -c   Shortname of compute node")
    print("      -t   The tenant/project ID")
    print("      -q   Suppress header line")
    sys.exit(2)

# Parse CLI options
try:
    opts,args = getopt.getopt(sys.argv[1:],"qn:c:t:")
except getopt.GetoptError:
    usage()

if not opts:
    usage()

for opt, arg in opts:
    if opt == "-q":
        quiet = True
    elif opt in "-n":
        if len(arg) < 4:
            print("4 Character minimum for name search!")
            sys.exit(2)
        vmlist = openstack.vm_list('hostname',arg)
    elif opt in "-c":
        vmlist = openstack.vm_list('cnode',arg)
    elif opt in "-t":
        vmlist = openstack.vm_list('tenant',arg)
    else:
        usage()

# Output
if not quiet:
   print("%s%-6s %-10s  %-32s  %-36s  %-9s  %s%s" % (bld,"CNODE","INSTANCE","TENANT","UUID","STATE","HOSTNAME",nrm))
for row in vmlist:
    instance_id,host,project_id,uuid,vm_state,hostname = row
    print("%-6s i-%08x  %-32s  %-36s  %-9s  %s" % (host,instance_id,project_id,uuid,vm_state,hostname))
