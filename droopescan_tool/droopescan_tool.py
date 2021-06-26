import subprocess
from pids import pids_of_token

def getDataFromDroopescan(url, token):
    if (token in pids_of_token.keys()):
        process = subprocess.Popen(['droopescan','scan','-u',url,'-o' 'json', '-t','10','-e','a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            pids_of_token[token].append(process.pid)
            process.wait()

            if (token in pids_of_token.keys()):
                pids_of_token[token].remove(process.pid)
                re, err = process.communicate()
                if (process.returncode != 1):
                    return re
                else:
                    return "Can not get data from droopescan"
            else:
                return "Can not get data from droopescan"
        except:
            return "Can not get data from droopescan"

    return "Can not get data from droopescan"