#!/usr/bin/env python

import ConfigParser
import MySQLdb

def get_nova_creds(db):
    config = ConfigParser.ConfigParser()
    config.read('ostools.cfg')

    name = config.get(db, 'name')
    user = config.get(db, 'user')
    password = config.get(db, 'pass')
    host = config.get(db, 'host')

    return (host,user,password,name)

def get_mysql_ver(db):
    # Setup variables
    dbhost,dbuser,dbpass,dbname = get_nova_creds(db)

    # Open the DB connection
    db = MySQLdb.connect(dbhost, dbuser, dbpass, dbname)
    cursor = db.cursor()

    # Execute the SQL command
    try:
        cursor.execute("SELECT version()")
        results = cursor.fetchone()
    except:
        print "Error: unable to fetch version"
        sys.exit(2)

    cursor.close()
    db.close()
    return results[0]

nova = get_mysql_ver('novadb')
kstn = get_mysql_ver('keystonedb')
#cndr = get_mysql_ver('cinderdb')
#glnc = get_mysql_ver('glancedb')

print("    Nova MySQL Version: %s" % nova )
print("Keystone MySQL Version: %s" % kstn )
#print("  Cinder MySQL Version: %s" % cndr )
#print("  Glance MySQL Version: %s" % glnc )

