# -*- coding: utf-8 -*-
"""
Created on Thu May 12 13:13:44 2016

@author: txinto
"""


import urllib
def import_URL(URL):
    exec urllib.urlopen(URL).read() in globals()
    
    
import_URL("http://gatatac.org:5555/sweep_exes.py")

if (sweep_id_to_execute != 0):
    import_URL("http://gatatac.org:5555/sweep_exes/"+str(sweep_id_to_execute)+".py")

