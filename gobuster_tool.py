import subprocess

def getDirsFromGobuster(url, cookie):
    results = subprocess.run(['gobuster','dir','--random-agent', '-u', url, '-w','SecLists/Discovery/Web-Content/directory-list-2.3-small.txt','-c',cookie, '-t','100','-q', '-z', '--no-error'],capture_output=True)
    if (results.returncode != 1):
        return (results.stdout)
    else:
        return "wrong URL"

def getFilesFromGobuster(url, cookie):
    results = subprocess.run(['gobuster','dir','--random-agent', '-u', url, '-w','SecLists/Discovery/Web-Content/raft-small-files.txt','-c',cookie, '-t','100','-q', '-z', '--no-error'],capture_output=True)
    if (results.returncode != 1):
        return (results.stdout)
    else:
        return "wrong URL"