#!/usr/bin/env python

import ConfigParser
import os

def get_version():
    config = ConfigParser.ConfigParser()
    config.read('ostools.cfg')
    version = config.get('release', 'version')
    return version

def rm(afile):
    try:
        os.remove(afile)
    except:
        pass

version = get_version()

rm("ostools.py")
rm("email_list")
rm("secgroup_list")
rm("vm_info")
rm("vm_list")
rm("tenant_info")
rm("tenant_list")
rm("volume_list")
rm("volume_info")

os.symlink(version+"_ostools.py","ostools.py")
os.symlink(version+"_email_list.py","email_list")
os.symlink(version+"_secgroup_list.py","secgroup_list")
os.symlink(version+"_vm_info.py","vm_info")
os.symlink(version+"_vm_list.py","vm_list")
os.symlink(version+"_flips.py","flips")
os.symlink(version+"_tenant_info.py","tenant_info")
os.symlink(version+"_tenant_list.py","tenant_list")
if version != 'diablo':
   os.symlink(version+"_volume_list.py","volume_list")
   os.symlink(version+"_volume_info.py","volume_info")

