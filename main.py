#!/usr/bin/env python
from utilities import *
import os
import sys
import shlex
import re
import ConfigParser
import logging
import logging.config
import optparse
import glob

def getIP():
    str_cmd = "curl http://www.whatbemyip.com"
    data = exec_cmd(str_cmd)
    if(data[0] != 0):
        return -1
    output = data[1]
    output= output.lower()
    ndx = re.search("\<h1 .*?\>", output )
    output = output[ndx.end():]
    ndx = re.search("<",output)
    output = output[:ndx.start()]
    ndx = re.search("\d",output)
    output = output[ndx.start():]
    res = re.match("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}",output)
    if(res == None):
        return -1
    else:
        return output

def getFirstOctet(ip):
    ndx = re.search("\.", ip )
    if(ndx == None):
        return -1;
    else:
        str_val = ip[:ndx.start()]
        return int(str_val)

def extractIP(value):
    #is there an IP contained.
    ndx = re.match(".*?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}.*", value)
    if(ndx == None):
        return -1
    
    start_ndx = re.search(".*?\d{1,3}\.", value)
    end_ndx = re.search(".*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",value)
    value = value[start_ndx.end()-4:end_ndx.end() ]
    value = value.replace("/t","")
    value = value.replace(" ","")
    ##found
    return value

def isMatch(value):
    ndx = re.match(".*?IN.*?A.*?\d", value)
    if(ndx == None):
        return False
    val = extractIP(value)
    if(val == -1):
        return False
    ##check IP
    if(getFirstOctet(val) != 192):
        return True;
    return False

def updateReadData(data,ip):
    for index in range(0,len(data)):
        item = data[index]
        if(isMatch(item)):
            res = re.sub("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", ip, item)
            if(res != None):
                data[index] = res
    return data

def processDomains(domain, ip ):
    handle = open(domain, "r")
    data = handle.readlines()
    handle.close()

    updateReadData(data,ip)
    cmd = "mv %s %s.original"%(domain,domain)
    print cmd
    exec_cmd(cmd)
    f = open(domain, "w")
    f.writelines(data)
    f.close()
    exec_cmd("rm %s.original"%(domain))

def getDomains(foobar):
    f= open(foobar,'r')
    if(f==None):
        print "error"
        return None
    data = f.readlines()
    for index in range(0,len(data)):
        item = data[index] 
        item = item.strip()
        item = item.replace("\n","")
        data[index] = item

    f.close()
    return data

def main():
    p = optparse.OptionParser()
    p.add_option('--domains', '-d', default="domains.txt",help="Passes a file containg list of files to modify")
    p.add_option('--ip', '-i', default="0",help="Override the IP address")
    options, arguments = p.parse_args()


    domains = getDomains(options.domains)

    ip = options.ip
    if(ip == "0"):
        ip = getIP()
    for d in domains:
        processDomains(d,ip)

if __name__ == '__main__':
    main()


