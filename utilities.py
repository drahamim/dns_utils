import math
import logging
import logging.config
import subprocess as sub
import shlex
import glob
import sys


global logger
logger = None

def printBlob(raw):
    if(type(raw) != type("")):
        logger.warning("sorry could not process since data passed in isn't a string ")
        return
    for i in raw.splitlines():
        logger.info(i)


def exec_cmd_glob(cmd, regex):
    """cmd should contain the special WRI value.  WRI is then 
    replaced by the appropriate regex """
    list = glob.glob(regex)
    status_code=-1
    out = ""
    for item in list:
        cmds = shlex.split(cmd)

        index=0
        for globItem in cmds:
            if(globItem == 'WRI'):
                cmds[index] = item
            index= index + 1

        try:
            job = sub.Popen(cmds ,stdout=sub.PIPE, stderr=sub.STDOUT)
            out += job.communicate()[0]
            status_code = job.poll()
            
        except:
            msg = "error executing: %s"%(cmds)
            ##fail safe in case logger didn't get created properly
            try:
                logger.error(msg)
            except:
                print msg

            return -1, msg

    status_code = 0
    return status_code, out

def exec_cmd(cmd):
    try:
        logger.info("Executing Command: " + str(cmd))
    except:
        ##If logger is Null, simply print
        print("Executing Command: " + str(cmd))

    try:
        job = sub.Popen(shlex.split(cmd),stdout=sub.PIPE, stderr=sub.STDOUT)
        out = job.communicate()[0]
        return job.poll(), out
    except:
            msg = "error executing: %s"%(cmd)
            ##fail safe in case logger didn't get created properly
            try:
                logger.error(msg)
            except:
                print msg

            return -1, msg



def getLogger(fileName):
    """If logger is Null, it will create a logger based the file configuration passed in, otherwise
       it will return the reference
    """

    if(logger == None):
        return setupLogger(fileName)
    else:
        return logger

##default size limit is 100megs
def setupLogger(fileName, logName='foobar.log',limit=104857600,count=10):
    """Readers the configuration file in the current directory, if the file 
       does not exist, then use the default configuration initialized below,
       sending output to decoder.log and standard output
    """
    global logger
    try:
        logging.config.fileConfig(fileName)
        logger = logging.getLogger("default")
    except:
        print "Uh-oh.. create a default logger"
        logger = logging.getLogger('default')
        logger.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.handlers.RotatingFileHandler(logName, maxBytes=limit, backupCount=count)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

if __name__ == '__main__':
    print "%s is a module and should not be executed directly.  Please run main.py"%(__file__)

