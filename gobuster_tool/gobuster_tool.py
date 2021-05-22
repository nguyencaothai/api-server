import subprocess
dictionary = '/root/python_tool/SecLists/Discovery/Web-Content/directory-list-2.3-small.txt'

def getDirsFromGobuster(url, cookie):
    results = subprocess.run(['gobuster','dir','--random-agent', '-u', url, '-w', dictionary,'-c',cookie, '-t','20','-q', '-z', '--no-error'], capture_output=True)
    if (results.returncode != 1):
        return (results.stdout)
    else:
        return "wrong URL"

def getFilesFromGobuster(url, cookie):
    results = subprocess.run(['gobuster','dir','--random-agent', '-u', url, '-w', dictionary,'-c',cookie, '-t','20','-q', '-z', '--no-error'], capture_output=True)
    if (results.returncode != 1):
        return (results.stdout)
    else:
        return "wrong URL"