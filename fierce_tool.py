import subprocess
import sys

def getDataFromFierce(url):

    sys.path.append('/root/python_tool/fierce/')

    subprocess.run(['rm','fierce_results.txt'], cwd='/root/python_tool/fierce')
    results = subprocess.run(['perl','fierce.pl','-file','fierce_results.txt','-dns',url], cwd='/root/python_tool/fierce', capture_output=True)
    if (results.returncode != 1):
        return True
    else:
        return False
