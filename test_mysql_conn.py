#!/usr/bin/env python

import ConfigParser
import MySQLdb

def get_nova_creds():
    config = ConfigParser.ConfigParser()
    config.read('ostools.cfg')

    name = config.get('novadb', 'name')
    user = config.get('novadb', 'user')
    password = config.get('novadb', 'pass')
    host = config.get('novadb', 'host')

    return (host,user,password,name)

# Setup variables
dbhost,dbuser,dbpass,dbname = get_nova_creds()

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

print("MySQL Version: %s" % results[0] )

