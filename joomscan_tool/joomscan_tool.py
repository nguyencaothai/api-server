import subprocess
import sys
import os


def getDataFromJoomscan(url):
    
    # Change directory to joomscan folder
    # sys.path.append('/root/python_tool/joomscan/')
    #sys.path.append('/root/python_tool/joomscan')
    sys.path = []
    sys.path.append('/root/python_tool/joomscan/')

    # Delete all old report
    subprocess.run('rm -rf reports/*', shell=True, cwd='/root/python_tool/joomscan')

    # Run command
    results = subprocess.run(['perl','joomscan.pl','--url',url,'-ec'], cwd='/root/python_tool/joomscan',capture_output=True)
    if (results.returncode != 1):
        return True
    else:
        return False
