from __future__ import print_function
import sys
import os
import getopt
import cloudbees
import requests
import fdeploy
import logging
import re

# fdeploy revision
fdeploy_version = "fdeploy-${project.version} ${buildNumber.timestamp}"
fdeploy.MUTE_ALL=True
logging.basicConfig(format='(%(filename)s:%(module)s:%(lineno)d) - %(funcName)s: %(message)s',level=logging.CRITICAL)
requests.packages.urllib3.connectionpool.log.disabled=True
try: # Python 2.7+
    from logging import NullHandler
    logging.getLogger('fdeploy').addHandler(logging.NullHandler())
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass
    logging.getLogger('fdeploy').addHandler(NullHandler())

# disable_warnings warnings SSL
try:
    requests.packages.urllib3.disable_warnings()
except AttributeError as ar:
    pass
# fdeploy revision
fdeploy_version = "fdeploy-${project.version} ${buildNumber.timestamp}"



if __name__ == "__main__":
    __args = sys.argv
    # strip of the test arguments and take
    #print str(__args)
    if __args[0]=='python -m unittest':
        idx = [i for i, item in enumerate(__args) if re.search('test_.*py$', item)]
        if idx and idx[0] > 0:
            __args = __args[idx[0]:]

        try:
            if __args.index('TestCloudbees.TestCloudbees') > 0:
                __args = __args[__args.index('TestCloudbees.TestCloudbees'):]
        except:
            pass
    elif 'py.test' in __args[0] or 'pytest' in __args[0]:
        idx = [i for i, item in enumerate(__args) if item == '-d']
        if idx[0] > 0:
            __args = __args[idx[0]-1:]
    else:
        pass
    #print(" main ", __args)
    exitcode=cloudbees.main(__args[1:])
    if  type(exitcode) != str and 'py.test' not in sys.argv[0] and 'pytest' not in sys.argv[0] and not sys.argv[0]!='python -m unittest' and not sys.argv[0].startswith('suite'):
        sys.exit(exitcode)
