import subprocess

def getDataFromWafw00f(url):

    results = subprocess.run(['wafw00f','-a','-o','wafw00f.json',url],capture_output=True)

    if (results.returncode != 1):
        return True
    else:
        return False
