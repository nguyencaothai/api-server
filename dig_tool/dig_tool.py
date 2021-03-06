import subprocess
from tldextract import extract

records = ['A','AAAA','ANY','CAA','CNAME','MX','NS','PTR','SOA','SRV','TXT']

def getDataFromDig(url):
    results = {}
    # Get domain name
    tsd, td, tsu = extract(url)
    url = td + '.' + tsu
    
    # Get all information of each record
    for record in records:
        tmp = []
        contents = subprocess.run(['dig',url,record,'+answer'],capture_output=True)
        if (contents.returncode != 1):
            results[record] = contents.stdout.decode('utf-8')
        else:
            results[record] = []    
    return results