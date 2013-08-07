Openstack Adminstrators Tool Set

Pre-requisites
==============
python (2.7+)
python-mysqldb


Instructions
============
1. Copy 'ostools.cfg.TEMPLATE' to 'ostools.cfg'
2. Edit 'ostools.cfg'
3. Test the configuration file with 'parse_config.py'
4. Test the configuration with 'test_mysql_conn.py'
5. Run 'configure_ostools.py'


Notes
=====
If you want to disable all colorized output edit ostools.py & set "colorize = False".
This is useful for removing the escape codes in output redirects to a file.


Scripts
=======
"flips" is a Floating IP Report that shows usage stats & top wasteful offenders for the Floating IP pool

Usage: ./email_list [ -c <CNODE> | -t <TENANT_ID> ] -s -q
      -c   Shortname of compute node
      -t   The tenant/project ID
      -s   Semicolon separated
      -q   Suppress header

Usage: ./secgroup_list [ -u <UUID> | -i <INSTANCE> | -p <PRIVATE_IP> | -f <FLOATING_IP> ]
      -u   UUID of instance
      -i   INSTANCE name [XXXXXXXX, i-XXXXXXXX, instance-XXXXXXXX]
      -p   Private IP Address of instance
      -f   Floating IP Address of instance

Usage: ./tenant_info [ -n <TENANT_NAME> | -t <TENANT_ID> ]
      -n   The tenant name OR partial match (4 character minimum)
      -t   The tenant/project ID
      -u   Display user list
      -q   Display quota information    <--- NOT available in Essex or Diablo
      -f   List allocated floating IP's

Usage: ./tenant_list -q [-h]
      -h   Help message
      -q   Suppress header line

Usage: ./vm_info [ -u <UUID> | -i <INSTANCE> | -p <PRIVATE_IP> | -f <FLOATING_IP> ]
      -u   UUID of instance
      -i   INSTANCE name [XXXXXXXX, i-XXXXXXXX, instance-XXXXXXXX]
      -p   Private IP Address of instance
      -f   Floating IP Address of instance

Usage: ./vm_list [ -c <CNODE> | -t <TENANT_ID> ] -q
      -c   Shortname of compute node
      -t   The tenant/project ID
      -q   Suppress header line

(NOT available in Diablo)
Usage: ./volume_list [ -c <CNODE> | -t <TENANT_ID> ] -q
      -c   Shortname of compute node
      -t   The tenant/project ID

