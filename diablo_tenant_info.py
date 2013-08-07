#!/usr/bin/env python

from ostools import *
import sys,getopt

openstack = OSTools('ostools.cfg')
domain = '@att.com'
do_user_list = False
do_list_ips = False

def usage():
    print("Usage: %s [ -n <TENANT_NAME> | -t <TENANT_ID> ]" % sys.argv[0])
    print("      -n   The tenant name OR partial match (4 character minimum)")
    print("      -t   The tenant/project ID")
    print("      -u   Display user list")
    print("      -f   List allocated floating IP's")
    sys.exit(2)

# Parse CLI options
try:
    opts,args = getopt.getopt(sys.argv[1:],"n:t:uf")
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
    elif opt in "-f":
        do_list_ips = True
    else:
        usage()

# OUTPUT
print
for tenant in tenant_matches:
    print("Tenant Name: %s" % tenant[1])
    print("Tenant ID:   %s" % tenant[0])
    print("Enabled:     %s" % bool(tenant[3]))
    print("Description: %s" % tenant[2])

    if do_user_list:
        print
        print("%s%-8s %-32s %-32s %s%s" % (bld, "USERID", "NAME", "EMAIL", "DEFAULT_TENANT", nrm))
        userlist = openstack.users_by_tenant(tenant[0])
        for userid in userlist:
            user_info = openstack.user_info_by_id(userid[0])
            username = user_info[0]
            default_tenant = user_info[1]
            if '@' in username:
                email = username
            else:
                email = username + domain
            print("%-8s %-32s %-32s %s" % (userid[0], username, email, default_tenant))

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
