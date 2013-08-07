#!/usr/bin/env python

from ostools import *
import sys,getopt

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
    print("%s%-40s %-10s %-8s %-32s%s" % (bld, "TENANT NAME", "TENANTID", "ENABLED", "DESCRIPTION",nrm))

for tenant in tenant_list:
    tenant_id = tenant[0]
    tenant_name = tenant[1]
    tenant_desc = tenant[2]
    tenant_enab = bool(tenant[3])

    if not tenant_desc:
        tenant_desc = '--'

    print("%-40s %-10s %-8s %-32s" % (tenant_name, tenant_id, tenant_enab, tenant_desc))

