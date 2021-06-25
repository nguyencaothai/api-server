import subprocess
from pids import pids_of_token

dictionary = '/root/python_tool/SecLists/Discovery/Web-Content/directory-list-2.3-small.txt'
# dictionary = '/root/python_tool/test.txt'

def getDirsFromGobuster(url, cookie, token):
    if (token in pids_of_token.keys()):
        process = subprocess.Popen(['gobuster','dir','--random-agent', '-u', url, '-w', dictionary,'-c',cookie, '-t','10','-q', '-z', '--no-error'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pids_of_token[token].append(process.pid)

        # If process finish successfully
        process.wait()
        if (token in pids_of_token.keys()):
            pids_of_token[token].remove(process.pid)
            re, err = process.communicate()
            if (process.returncode != 1):
                return (re)
            else:
                return "wrong URL"
        else:
            return "wrong URL"

    return "wrong URL"

def getFilesFromGobuster(url, cookie, token):
    if (token in pids_of_token.keys()):
        process = subprocess.Popen(['gobuster','dir','--random-agent', '-u', url, '-w', dictionary,'-c',cookie, '-t','10','-q', '-z', '--no-error'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pids_of_token[token].append(process.pid)

        # If process finish successfully
        process.wait()
        if (token in pids_of_token.keys()):
            pids_of_token[token].remove(process.pid)
            re, err = process.communicate()
            if (process.returncode != 1):
                return (re)
            else:
                return "wrong URL"
        else:
            return "wrong URL"

    return "wrong URL"