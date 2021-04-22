import subprocess
import os
import sys

def getDataFromJoomscan(url):
    
    # Change directory to joomscan folder
    # sys.path.append('/root/python_tool/joomscan/')
    os.chdir('/root/python_tool/joomscan')

    # Delete all old report
    subprocess.run('rm -rf reports/*', shell=True)

    # Run command
    results = subprocess.run(['perl','joomscan.pl','--url',url,'-ec'],capture_output=True)
    if (results.returncode != 1):
        return True
    else:
        return False