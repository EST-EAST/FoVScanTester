# -*- coding: utf-8 -*-
"""
Retrieves an scanning algorithms list from the given web server, and allows the user to execute one of them
"""

import os
import urllib
import sweepconfig

def import_URL(URL):
    exec urllib.urlopen(URL).read() in globals()
    
menurl = sweepconfig.cte_web_root+"/scan_exes"
print "Running on "+os.name
print "The menu chooser will be downloaded from "+menurl+".py"
print "The list of avaliable algorithms are here: "+menurl
import_URL(menurl+".py")

if (scan_id_to_execute != 0):
    sweepurl=sweepconfig.cte_web_root+"/scan_exes/"+str(scan_id_to_execute)
    print "The algorithm to be downloaded is "+sweepurl+".py"
    print "It corresponds to the one described at "+sweepurl
    import_URL(sweepurl+".py")

