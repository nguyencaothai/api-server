import subprocess

def getDataFromWafw00f(url, token):

    reportName = 'wafw00f_' + token + '.report'
    subprocess.run(['rm', reportName], cwd='/root/python_tool/wafw00f_tool')

    results = subprocess.run(['wafw00f','-a', '-f','json', '-o', reportName,url],capture_output=True, cwd='/root/python_tool/wafw00f_tool/')

    if (results.returncode != 1):
        return True
    else:
        return False
