#!/usr/bin/env python

import ConfigParser
import MySQLdb
import os


# Terminal info
colorize = True
if os.environ['TERM'] == "xterm" and colorize:
   bld = "\033[1m"       # bold
   uln = "\033[4m"       # underline
   nrm = "\033[0m"       # reset
   red = "\033[01;31m"   # hi red
   grn = "\033[01;32m"   # hi green
   ylw = "\033[01;33m"   # hi yellow
   blu = "\033[01;34m"   # hi blue
   vlt = "\033[01;35m"   # hi violet
   cyn = "\033[01;36m"   # hi cyan
   wht = "\033[01;37m"   # hi white
else:
   bld = ''
   uln = ''
   nrm = ''
   red = ''
   grn = ''
   ylw = ''
   blu = ''
   vlt = ''
   cyn = ''
   wht = ''


class OSTools:

    def __init__(self, configfile):
        self.configfile = configfile


    def __query(self, querystr, name, db, cnt=None):
        self.dbhost,self.dbuser,self.dbpass,self.dbname = self.__db_creds(self.configfile, db)
        self.db = MySQLdb.connect(self.dbhost,self.dbuser,self.dbpass,self.dbname)
        self.cursor = self.db.cursor()

        try:
            self.cursor.execute(querystr)
        except:
            print("Error: [%s]" % name)

        if cnt:
            results = self.cursor.fetchone()
            self.__dbclose()
            return results
        else:
            results = self.cursor.fetchall()
            self.__dbclose()
            return results


    def __dbclose(self):
        self.cursor.close()
        self.db.close()

         
    def __db_creds(self, configfile, db):
        config = ConfigParser.ConfigParser()

        try:
            config.read(configfile)
        except:
            print("Unable to open config file: %s" % configfile)
            sys.exit(1)

        name = config.get(db, 'name')
        user = config.get(db, 'user')
        password = config.get(db, 'pass')
        host = config.get(db, 'host')

        return (host,user,password,name)


    def vm_list(self, key, val):
        if key == "cnode":
            querystr = "SELECT id,host,project_id,uuid,vm_state,hostname \
                        FROM instances \
                        WHERE host='%s' AND deleted=0" % (val)
        elif key == "tenant":
            querystr = "SELECT id,host,project_id,uuid,vm_state,hostname \
                        FROM instances \
                        WHERE project_id='%s' AND deleted=0" % (val)
        elif key == "hostname":
            querystr = "SELECT id,host,project_id,uuid,vm_state,hostname \
                        FROM instances \
                        WHERE deleted=0 AND hostname like '%%%s%%'" % (val)

        results = self.__query(querystr, 'vm_list', 'novadb')
        return results


    def vm_info(self, key, val):
        if key == "uuid":
            querystr = "SELECT user_id,created_at,id,project_id,vm_state,hostname,host,uuid \
                        FROM instances \
                        WHERE deleted=0 AND uuid='%s'" % (val)
        elif key == "instance":
            querystr = "SELECT user_id,created_at,id,project_id,vm_state,hostname,host,uuid \
                        FROM instances \
                        WHERE deleted=0 AND id='%s'" % (val)

        results = self.__query(querystr, 'vm_info', 'novadb', 1)
        return results


    def secgrpid_list(self, instanceid):
        querystr = "SELECT security_group_id \
                    FROM security_group_instance_association \
                    WHERE deleted=0 AND instance_id='%s'" % (instanceid)

        results = self.__query(querystr, 'secgrpid_list', 'novadb')
        return results


    def secgrp_name(self, groupid):
        querystr = "SELECT name FROM security_groups WHERE id='%s'" % (groupid)

        results = self.__query(querystr, 'secgrp_name', 'novadb', 1)
        return results[0]


    def secgrp_rule_list(self, groupid):
        querystr = "SELECT protocol,from_port,to_port,cidr \
                    FROM security_group_rules \
                    WHERE deleted=0 AND parent_group_id='%s'" % (groupid)

        results = self.__query(querystr, 'secgrp_rule_list', 'novadb')
        return results


    def instanceid_by_fixedip(self, address):
        querystr = "SELECT instance_id \
                    FROM fixed_ips \
                    WHERE deleted=0 AND address='%s'" % (address)

        results = self.__query(querystr, 'instanceid_by_fixedip', 'novadb', 1)
        return results[0]


    def instanceid_by_floatingip(self, address):
        querystr = "SELECT fixed_ip_id \
                    FROM floating_ips \
                    WHERE deleted=0 AND address='%s'" % (address)


        fixedipid = self.__query(querystr, 'instanceid_by_floatingip 1', 'novadb', 1)

        querystr = "SELECT instance_id \
                    FROM fixed_ips \
                    WHERE deleted=0 AND id='%s'" % (fixedipid[0])

        results = self.__query(querystr, 'instanceid_by_floatingip 2', 'novadb', 1)
        return results[0]


    def uuid_by_instanceid(self, instanceid):
        querystr = "SELECT uuid \
                    FROM instances \
                    WHERE deleted=0 AND id='%s'" % (instanceid)

        results = self.__query(querystr, 'uuid_by_instanceid', 'novadb', 1)
        return results[0]


    def fixedip_by_instanceid(self, instanceid):
        querystr = "SELECT address \
                    FROM fixed_ips \
                    WHERE deleted=0 AND instance_id='%s'" % (instanceid)

        results = self.__query(querystr, 'fixedip_by_instanceid', 'novadb', 1)
        return results[0]


    def fixedipid_by_instanceid(self, instanceid):
        querystr = "SELECT id \
                   FROM fixed_ips \
                   WHERE deleted=0 AND instance_id='%s'" % (instanceid)


        results = self.__query(querystr, 'fixedipid_by_instanceid', 'novadb', 1)
        return results[0]


    def floatingips_by_fixedipid(self, fixedipid):
        querystr = "SELECT address \
                    FROM floating_ips \
                    WHERE deleted=0 AND fixed_ip_id='%s'" % (fixedipid)

        results = self.__query(querystr, 'floatingips_by_fixedipid', 'novadb')
        return results


    def tenant_name(self, tenantid):
        querystr = "SELECT name FROM tenants WHERE id='%s'" % (tenantid)

        results = self.__query(querystr, 'tenant_name', 'keystonedb', 1)
        return results[0]


    def tenant_info_by_name(self, tenant_name):
        # id,name,desc,enabled
        querystr = "SELECT * FROM tenants WHERE name like '%%%s%%'" % (tenant_name)

        results = self.__query(querystr, 'tenant_info_by_name', 'keystonedb')
        return results


    def tenant_info_by_tenantid(self, tenantid):
        # id,name,desc,enabled
        querystr = "SELECT * FROM tenants WHERE id='%s'" % (tenantid)

        results = self.__query(querystr, 'tenant_info_by_tenantid', 'keystonedb')
        return results


    def tenant_list(self):
        # id,name,desc,enabled
        querystr = "SELECT * FROM tenants ORDER BY name"

        results = self.__query(querystr, 'tenant_list', 'keystonedb')
        return results


    def users_by_tenant(self, tenantid):
        querystr = "SELECT DISTINCT user_id FROM user_roles WHERE tenant_id='%s'" % (tenantid)

        results = self.__query(querystr, 'users_by_tenant', 'keystonedb')
        return results


    def user_info_by_id(self, userid):
        querystr = "SELECT name,tenant_id FROM users WHERE id='%s'" % (userid)

        results = self.__query(querystr, 'users_info_by_id', 'keystonedb', 1)
        return results


    def email_by_userid(self, userid):
        querystr = "SELECT name FROM users WHERE id='%s'" % (userid)

        results = self.__query(querystr, 'email_by_userid', 'keystonedb', 1)
        return results[0]


    def floating_ips(self, tenantid):
        querystr = "SELECT floating_ips.address, instances.hostname, instances.uuid \
                    FROM floating_ips \
                    LEFT JOIN fixed_ips ON floating_ips.fixed_ip_id = fixed_ips.id \
                    LEFT JOIN instances ON fixed_ips.instance_id = instances.id \
                    WHERE floating_ips.deleted = 0 \
                    AND floating_ips.project_id = '%s'" % tenantid

        results = self.__query(querystr, 'floating_ips', 'novadb')
        return results


class Flips:

    def __init__(self, configfile):
        self.configfile = configfile

        # Total floating IP count
        query1 = "SELECT count(*) FROM floating_ips"
        # Total free floating IP count
        query2 = "SELECT count(*) FROM floating_ips WHERE deleted=0 AND project_id IS NULL"
        # Total allocated, but unused IP count
        query3 = "SELECT count(*) FROM floating_ips WHERE deleted=0 AND host IS NULL AND project_id IS NOT NULL"
        # Tenants by allocated floating IP count
        query4 = "SELECT project_id, count(*) AS count \
                  FROM floating_ips \
                  WHERE deleted=0 \
                  AND project_id IS NOT NULL \
                  GROUP BY project_id \
                  ORDER BY count"
        # Tenants by allocated, but unused floating IP count
        query5 = "SELECT project_id, count(*) AS count \
                  FROM floating_ips \
                  WHERE deleted=0 \
                  AND project_id IS NOT NULL \
                  AND host IS NULL \
                  GROUP BY project_id \
                  ORDER BY count"
        # Tenants by allocated, but unused for >1 month floating IP count
        query6 = "SELECT project_id,count(address) AS idle_ips \
                  FROM floating_ips \
                  WHERE deleted=0 \
                  AND project_id IS NOT NULL \
                  AND host IS NULL \
                  AND updated_at <= date_sub( curdate(), interval 1 month ) \
                  GROUP BY project_id \
                  ORDER BY idle_ips"


        self.total_flips  = self.__query(query1, 'Total Floating IPs', 'novadb', 1)
        self.free_flips   = self.__query(query2, 'Free Floating IPs', 'novadb', 1)
        self.idle_flips   = self.__query(query3, 'Idle Floating IPs', 'novadb', 1)
        self.alloc_count  = self.__query(query4, 'Allocated Floating IPs', 'novadb')
        self.alloc_unused = self.__query(query5, 'Allocated-Unused Floating IPs', 'novadb')
        self.alloc_idlemo = self.__query(query6, 'Allocated-Unused >1mo Floating IPs', 'novadb')


    def __query(self, querystr, name, db, cnt=None):
        self.dbhost,self.dbuser,self.dbpass,self.dbname = self.__db_creds(self.configfile, db)
        self.db = MySQLdb.connect(self.dbhost,self.dbuser,self.dbpass,self.dbname)
        self.cursor = self.db.cursor()

        try:
            self.cursor.execute(querystr)
        except:
            print("Error: [%s]" % name)

        if cnt:
            results = self.cursor.fetchone()
            self.__dbclose()
            return results
        else:
            results = self.cursor.fetchall()
            self.__dbclose()
            return results


    def __dbclose(self):
        self.cursor.close()
        self.db.close()


    def __db_creds(self, configfile, db):
        config = ConfigParser.ConfigParser()

        try:
            config.read(configfile)
        except:
            print("Unable to open config file: %s" % configfile)
            sys.exit(1)

        name = config.get(db, 'name')
        user = config.get(db, 'user')
        password = config.get(db, 'pass')
        host = config.get(db, 'host')

        return (host,user,password,name)


    def tenant_name(self, tenantid):
        querystr = "SELECT name FROM tenants WHERE id='%s'" % (tenantid)

        results = self.__query(querystr, 'tenant_name', 'keystonedb', 1)
        return results[0]

