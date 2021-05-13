import subprocess

def getDataFromCmseek(url):
    
    subprocess.run('rm -rf Result/*', shell=True, cwd='/root/python_tool/CMSeeK')

    results = subprocess.run(['python','cmseek.py','-u',url,'--batch'], cwd='/root/python_tool/CMSeeK/', capture_output=True)
    if (results.returncode != 1):
        return (results.stdout)
    else:
        return "Can not get data from cmseek"