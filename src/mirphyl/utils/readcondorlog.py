#! /usr/bin/env python
'''
Created on Jul 19, 2011

@author: smirarab
'''
import sys
import subprocess
import re
from datetime import timedelta

def get_mem_result():    
    res, err = subprocess.Popen(
                    ["grep", "Image size of job updated", condor_file],
                    stderr=subprocess.PIPE,stdout=subprocess.PIPE).communicate()
    return res.split("\n")[-2].split()[-1]
    
    
def get_result(key):    
    res, err = subprocess.Popen(
                    ["grep", key, condor_file],
                    stderr=subprocess.PIPE,stdout=subprocess.PIPE).communicate()
    resline = res.split("\n")[-2]
    timestr = pat.sub( r"\1" , resline)
    
    d = re.match(
            r'((?P<days>\d+) )?(?P<hours>\d+):'
            r'(?P<minutes>\d+):(?P<seconds>\d+)',
            str(timestr)).groupdict(0)
    td = timedelta(**dict(( (key, int(value))
                              for key, value in d.items() )))
    return ((td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6)

if __name__ == '__main__':
    condor_file = sys.argv[1]
    out = open(sys.argv[2],"w") if len(sys.argv) > 2 else sys.stdout

    pat = re.compile(".*Usr (.*), Sys.*")
        
    d = get_result("Total Remote Usage")
    print >>out, "Total_time %d" %d 
        
    d = get_result("Run Remote Usage")
    print >>out, "Run_time %d" %d 
        
    s = get_mem_result()    
    print >>out, "Image_size %s" %s