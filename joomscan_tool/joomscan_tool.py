import subprocess
import sys
import os
from pids import pids_of_token

def getDataFromJoomscan(url, token):
    
    sys.path = []
    sys.path.append('/root/python_tool/joomscan/')

    # Delete all old report
    subprocess.run('rm -rf reports/*', shell=True, cwd='/root/python_tool/joomscan')

    if (token in pids_of_token.keys()):
        # Run command
        process = subprocess.Popen(['perl','joomscan.pl','--url',url,'-ec'], cwd='/root/python_tool/joomscan', stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        pids_of_token[token].append(process.pid)
        process.wait()

        if (token in pids_of_token.keys()):
            pids_of_token[token].remove(process.pid)
            re, err = process.communicate()
            if (process.returncode != 1):
                return True
            else:
                return False
        else:
            return False

    return False
