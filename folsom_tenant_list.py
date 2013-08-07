#!/usr/bin/env python

from ostools import *
import sys,getopt,json

openstack = OSTools('ostools.cfg')
quiet = False

def usage():
    print("Usage: %s -q [-h]" % sys.argv[0])
    print("      -h   Help message")
    print("      -q   Suppress header line")
    sys.exit(2)

# Parse CLI options
try:
    opts,args = getopt.getopt(sys.argv[1:],"hq")
except getopt.GetoptError:
    usage()

for opt, arg in opts:
    if opt == "-h":
        usage()
    if opt == "-q":
        quiet = True
    else:
        usage()

tenant_list = openstack.tenant_list()

# OUTPUT
if not quiet:
    print("%s%-32s %-33s %-8s %-32s%s" % (bld, "TENANT NAME", "TENANT ID", "ENABLED", "DESCRIPTION",nrm))

for tenant in tenant_list:
    tenant_id = tenant[0]
    tenant_name = tenant[1]
    tenant_extra = json.loads(tenant[2])

    # Pretty-up the output
    try:
        enabled = tenant_extra['enabled']
    except KeyError:
        enabled = "False"
    try:
        description = tenant_extra['description']
    except KeyError:
        description = ''

    print("%-32s %-33s %-8s %-32s" % (tenant_name, tenant_id, enabled, description))

