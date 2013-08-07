#!/usr/bin/env python

import os,ConfigParser

config = ConfigParser.ConfigParser()
config.read('ostools.cfg')

version = config.get('release', 'version')
novadb_user = config.get('novadb', 'user')
novadb_pass = config.get('novadb', 'pass')
novadb_name = config.get('novadb', 'name')
novadb_host = config.get('novadb', 'host')
ksdb_user = config.get('keystonedb', 'user')
ksdb_pass = config.get('keystonedb', 'pass')
ksdb_name = config.get('keystonedb', 'name')
ksdb_host = config.get('keystonedb', 'host')
gldb_user = config.get('glancedb', 'user')
gldb_pass = config.get('glancedb', 'pass')
gldb_name = config.get('glancedb', 'name')
gldb_host = config.get('glancedb', 'host')
cindb_user = config.get('cinderdb', 'user')
cindb_pass = config.get('cinderdb', 'pass')
cindb_name = config.get('cinderdb', 'name')
cindb_host = config.get('cinderdb', 'host')

print
print("OpenStack Version: %s" % version)
print
print("Nova DBUser: %s" % novadb_user)
print("Nova DBPass: %s" % novadb_pass)
print("Nova DBName: %s" % novadb_name)
print("Nova DBHost: %s" % novadb_host)
print
print("Keystone DBUser: %s" % ksdb_user)
print("Keystone DBPass: %s" % ksdb_pass)
print("Keystone DBName: %s" % ksdb_name)
print("Keystone DBHost: %s" % ksdb_host)
print
print("Glance DBUser: %s" % gldb_user)
print("Glance DBPass: %s" % gldb_pass)
print("Glance DBName: %s" % gldb_name)
print("Glance DBHost: %s" % gldb_host)
print
print("Cinder DBUser: %s" % cindb_user)
print("Cinder DBPass: %s" % cindb_pass)
print("Cinder DBName: %s" % cindb_name)
print("Cinder DBHost: %s" % cindb_host)
print
