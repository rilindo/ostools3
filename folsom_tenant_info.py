#!/usr/bin/env python

from ostools import *
import sys,getopt,json

openstack = OSTools('ostools.cfg')
do_user_list = False
do_quota_list = False
do_list_ips = False

def usage():
    print("Usage: %s [ -n <TENANT_NAME> | -t <TENANT_ID> ]" % sys.argv[0])
    print("      -n   The tenant name OR partial match (4 character minimum)")
    print("      -t   The tenant/project ID")
    print("      -u   Display user list")
    print("      -q   Display quota information")
    print("      -f   List allocated floating IP's")
    sys.exit(2)

def trunc(instr,length):
    return instr[:(length-1)] + red + "*" + nrm

# Parse CLI options
try:
    opts,args = getopt.getopt(sys.argv[1:],"n:t:uqf")
except getopt.GetoptError:
    usage()

if not opts:
    usage()

for opt, arg in opts:
    if opt == "-n":
        if len(arg) < 4:
            print("4 Character minimum for name search!")
            sys.exit(2)
        tenant_matches = openstack.tenant_info_by_name(arg)
    elif opt in "-t":
        tenant_matches = openstack.tenant_info_by_tenantid(arg)
    elif opt in "-u":
        do_user_list = True
    elif opt in "-q":
        do_quota_list = True
    elif opt in "-f":
        do_list_ips = True
    else:
        usage()

# OUTPUT
print
for tenant in tenant_matches:
    tenant_extra = json.loads(tenant[2])
    print("Tenant Name: %s" % tenant[1])
    print("Tenant ID:   %s" % tenant[0])
    try:
        print("Enabled:     %s" % tenant_extra['enabled'])
    except KeyError:
        print("Enabled:     False")
    try:
        print("Description: %s" % tenant_extra['description'])
    except KeyError:
        print("Description: None")

    if do_user_list:
        print
        print("%s%-33s %-20s %-32s %-32s%s" % (bld, "USERID", "NAME", "EMAIL", "DEFAULT_TENANT", nrm))
        userlist = openstack.users_by_tenant(tenant[0])
        for userid in userlist:
            user_info = openstack.user_info_by_id(userid[0])
            user_extra = json.loads(user_info[1])
            if len(user_info[0]) > 20:
                username = trunc(user_info[0],20)
            else:
                username = user_info[0]
            if len(user_extra['email']) > 32:
                email = trunc(user_extra['email'],32)
            else:
                email = user_extra['email']
            print("%-33s %-20s %-32s %-32s" % (userid[0], username, email, user_extra['tenantId']))

    if do_quota_list:
        print
        quotas = openstack.tenant_quotas(tenant[0])
        print("%s%-28s %-8s %-8s%s" % (bld, "RESOURCE", "HARD", "INUSE", nrm))
        for key in sorted(quotas.iterkeys()):
            print("%-27s: %-8s %-8s" % (key, quotas[key]['limit'], quotas[key]['inuse']))

    if do_list_ips:
        print
        floating_ips = openstack.floating_ips(tenant[0])
        print("%s%-16s %-37s %s%s" % (bld, "ADDRESS", "UUID", "HOSTNAME", nrm))
        for ip in floating_ips:
            address, hostname, uuid = ip

            if uuid is None:
                uuid = '--'
                hostname = '--'

            print("%-16s %-37s %s" % (address, uuid, hostname))
    print
    print
