#!/usr/bin/env python

from ostools import *

report = Flips('ostools.cfg')

print
print("%s%sFLOATING IP REPORT%s" % (bld,uln,nrm))
print
print("Total IP's: %s" % report.total_flips)
print(" Free IP's: %s" % report.free_flips)
print(" Idle IP's: %s" % report.idle_flips)
print
print("%sTop 10 Tenants - Allocated%s" % (blu,nrm))
print("%s%-5s %-33s %s%s" % (bld, "IP#", "TENANT ID", "TENANT NAME", nrm))
for x in range(-10,0):
    tenant_name = report.tenant_name(report.alloc_count[x][0])
    print("%-5s %-33s %s" % (report.alloc_count[x][1], report.alloc_count[x][0], tenant_name))
print
print("%sTop 10 Tenants - Idle%s" % (blu,nrm))
print("%s%-5s %-33s %s%s" % (bld, "IP#", "TENANT ID", "TENANT NAME", nrm))
for x in range(-10,0):
    tenant_name = report.tenant_name(report.alloc_unused[x][0])
    print("%-5s %-33s %s" % (report.alloc_unused[x][1], report.alloc_unused[x][0], tenant_name))
print
print("%sTop 10 Tenants - Idle >30 days%s" % (blu,nrm))
print("%s%-5s %-33s %s%s" % (bld, "IP#", "TENANT ID", "TENANT NAME", nrm))
for x in range(-10,0):
    tenant_name = report.tenant_name(report.alloc_idlemo[x][0])
    print("%-5s %-33s %s" % (report.alloc_idlemo[x][1], report.alloc_idlemo[x][0], tenant_name))

