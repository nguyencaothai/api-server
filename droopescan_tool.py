import subprocess

def getDataFromDroopescan(url):
    
    results = subprocess.run(['droopescan','scan','-u',url,'-o' 'json', '-t','50'],capture_output=True)
    if (results.returncode != 1):
        return (results.stdout)
    else:
        return "Can not get data from droopescan"