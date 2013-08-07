#!/usr/bin/env python

from ostools import *
import sys,getopt,json

openstack = OSTools('ostools.cfg')
quiet = False
separated = False
tenants= []
users = []

def usage():
    print("Usage: %s [ -c <CNODE> | -t <TENANT_ID> ] -s -q" % sys.argv[0])
    print("      -c   Shortname of compute node")
    print("      -t   The tenant/project ID")
    print("      -s   Semicolon separated")
    print("      -q   Suppress header")
    sys.exit(2)

# Parse CLI options
try:
    opts,args = getopt.getopt(sys.argv[1:],"sqc:t:")
except getopt.GetoptError:
    usage()

if not opts:
    usage()

for opt, arg in opts:
    if opt == "-q":
        quiet = True
    elif opt in "-s":
        separated = True
    elif opt in "-t":
        tenants.append(arg)
    elif opt in "-c":
        vmlist = openstack.vm_list('cnode',arg)
        for row in vmlist:
            tenants.append(row[2])
        tenants = set(tenants)
    else:
        usage()

for tenant in tenants:
    emails = []
    users = openstack.users_by_tenant(tenant)

    if not quiet:
        # There can be orphaned instances w/o a tenant in Keystone
        try:
            tenant_name = openstack.tenant_name(tenant)
            print("%s%s [%s]%s" % (blu, tenant_name, tenant, nrm))
        except:
            print("%sINVALID TENANT! [%s]%s" % (red, tenant, nrm))
            print
            continue

    for user in users:
        extra = json.loads(openstack.email_by_userid(user))
        if extra['email'] is not None:
            emails.append(extra['email'])

    if separated:
        print ";".join(emails)
    else:
        print "\n".join(emails)
    print
