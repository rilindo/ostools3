#!/usr/bin/env python

from ostools import *
import sys,getopt,json

openstack = OSTools('ostools.cfg')

def usage():
    print("Usage: %s [ -c <CNODE> | -t <TENANT_ID> ] -q" % sys.argv[0])
    print("      -c   Shortname of compute node")
    print("      -t   The tenant/project ID")
    sys.exit(2)

# Parse CLI options
try:
    opts,args = getopt.getopt(sys.argv[1:],"qc:t:")
except getopt.GetoptError:
    usage()

if not opts:
    usage()

for opt, arg in opts:
    if opt in "-c":
        # Get list of vm's on the compute node
        vm_list = openstack.vm_list('cnode', arg)
        # Loop thru each vm
        for vm in vm_list:
            # Chop the vm record into variables
            instid,host,project_id,uuid,vm_state,hostname = vm
            # Get volume information for this vm (if any exists)
            volume_list = openstack.volumes_by_instanceid(instid)
            # If volumes found, display them
            if volume_list:
                for volume in volume_list:
                    # Chop the volume record into variables
                    created_at,vol_id,user_id,project_id,size,instance_id, \
                    status,attach_status,display_name,display_description = volume
                    # Get the user_name
                    user_info = openstack.user_info_by_id(user_id)
                    try:
                        user_name = user_info[0]
                    except:
                        user_name = red + 'DELETED' + nrm
                    # Get the LUN
                    conn_info = json.loads(openstack.volume_lun(vol_id)) 
                    # Output
                    print
                    print("%s%s [%s]%s" % (blu, vol_id, display_name, nrm))
                    print("Created:  %s" % created_at)
                    print("Creator:  %s [%s]" % (user_id, user_name))
                    print("Tenant:   %s" % project_id)
                    print("Size:     %s GB" % size)
                    print("Descr:    %s" % display_description)
                    print("Status:   %s/%s" % (attach_status, status))
                    print("Attached: %s [%s]" % (uuid, hostname))
                    print("LUN:      %s:%s" % (host,conn_info['data']['device_path']))

    elif opt in "-t":
        volume_list = openstack.volumes_by_tenantid(arg)
        for volume in volume_list:
            # Chop the volume record into variables
            created_at,vol_id,user_id,project_id,size,instance_id, \
            status,attach_status,display_name,display_description = volume
            # Get the username
            user_info = openstack.user_info_by_id(user_id)
            try:
                user_name = user_info[0]
            except:
                user_name = red + 'DELETED' + nrm
            # Output
            print
            print("%s%s [%s]%s" % (blu, vol_id, display_name, nrm))
            print("Created:  %s" % created_at)
            print("Creator:  %s [%s]" % (user_id, user_name))
            print("Tenant:   %s" % project_id)
            print("Size:     %s GB" % size)
            print("Descr:    %s" % display_description)
            print("Status:   %s/%s" % (attach_status, status))
            # If we have an instance_id, then it's mounted, so display that.
            if instance_id:
                user_id,created_at,instid,project_id, \
                vm_state,hostname,host,uuid = openstack.vm_info('instance', instance_id)
                conn_info = json.loads(openstack.volume_lun(vol_id))
                print("Attached: %s [%s]" % (uuid, hostname))
                print("LUN:      %s:%s" % (host,conn_info['data']['device_path']))
    else:
        usage()

print
