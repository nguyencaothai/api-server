import subprocess
from tldextract import extract

def getDataFromCmseek(url):

    tsd, td, tsu = extract(url)
    url = tsd + '.' + td + '.' + tsu
    url = url[1: len(url)-1] if (url[0] == '.' and url[len(url)-1] == '.') else url[1:] if (url[0] == '.') else url[:len(url)-1] if (url[len(url)-1] == '.') else url

    if (url == ''):
        return "Can not get data from cmseek", None

    results = subprocess.run(['python','cmseek.py','-u',url,'--batch'], cwd='/root/python_tool/CMSeeK/', capture_output=True)
    if (results.returncode != 1):
        return (results.stdout, url)
    else:
        return "Can not get data from cmseek", None