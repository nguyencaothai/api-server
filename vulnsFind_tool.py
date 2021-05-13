import subprocess
import requests
import json
import re
from searchsploit_tool import getDataFromSearchsploit
from joomscan_tool.parseHTML import parseReportHTML

# Request to exploit-db.com
def requestToExploitDB(patterns):
    response = {'data':[]}

    try:
        response = requests.get(f"https://www.exploit-db.com/?draw=49&columns%5B0%5D%5Bdata%5D=date_published&columns%5B0%5D%5Bname%5D=date_published&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=download&columns%5B1%5D%5Bname%5D=download&columns%5B1%5D%5Bsearchable%5D=false&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=application_md5&columns%5B2%5D%5Bname%5D=application_md5&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=false&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=verified&columns%5B3%5D%5Bname%5D=verified&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=false&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=description&columns%5B4%5D%5Bname%5D=description&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=false&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=type_id&columns%5B5%5D%5Bname%5D=type_id&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=false&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=platform_id&columns%5B6%5D%5Bname%5D=platform_id&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=false&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=author_id&columns%5B7%5D%5Bname%5D=author_id&columns%5B7%5D%5Bsearchable%5D=false&columns%5B7%5D%5Borderable%5D=false&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=code&columns%5B8%5D%5Bname%5D=code.code&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=id&columns%5B9%5D%5Bname%5D=id&columns%5B9%5D%5Bsearchable%5D=false&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=9&order%5B0%5D%5Bdir%5D=desc&start=0&length=15&search%5Bvalue%5D={patterns}&search%5Bregex%5D=false&author=&port=&type=&tag=&platform=&_=1619485206457", headers={'X-Requested-With':'XMLHttpRequest'})
        return json.loads(response.text)
    except:
        return response

def requestToLocalExploitDB(patterns):

    print(patterns)
    path = 'https://www.exploit-db.com/raw/'
    results = getDataFromSearchsploit(patterns)
    contents = {}
    contents['RESULTS_EXPLOIT'] = []

    if (results):
        with open('searchsploit_results.json', 'r') as f:
            contents = json.loads(f.read())
            # Delete un-needed elements
            contents.pop('SEARCH')
            contents.pop('DB_PATH_EXPLOIT')
            contents.pop('DB_PATH_SHELLCODE')
            contents.pop('RESULTS_SHELLCODE')
                
            for i in range(0, len(contents['RESULTS_EXPLOIT'])):
                edb_id = contents['RESULTS_EXPLOIT'][i]['EDB-ID']
                contents['RESULTS_EXPLOIT'][i].pop('EDB-ID')
                contents['RESULTS_EXPLOIT'][i].pop('Path')
                contents['RESULTS_EXPLOIT'][i]['URL'] = path + edb_id
        return contents
    else:
        return contents

def getVulnsForWebTech(technologies):
    vulns = []
    for technology in technologies:
        if (technology['version'] != None):
            # Build patterns for searching on ExploitDB
            patterns = technology['name'] + '%20' + technology['version']
            results = requestToExploitDB(patterns)
            vulns = vulns + results['data']
        else:
            continue
    return vulns

def getVulnsForWhatWeb(technologies):
    vulns = []
    for technology in technologies:
        if ('version' in technology.keys()):
            patterns = technology['name'] + '%20' + technology['version']
            results = requestToExploitDB(patterns)
            vulns = vulns + results['data']
        else:
            continue
    return vulns

def getVulnsForNmap():
    vulns = []
    results = subprocess.run(['searchsploit','-json','--colour','--nmap','nmap_results_xml'], capture_output=True)
    if (results.returncode != 1):
        results = results.stdout.decode('utf-8').replace('\n\n\n','\n').replace('\n\t\t','').replace('\n\t','').replace('\t','')
        results = re.sub(r']\n}',']}', results)
        results = results.split('\n')
        for index in range(len(results) - 1):
            result = json.loads(results[index])
            vulns = vulns + result['RESULTS_EXPLOIT']
    return vulns

def getVulnsForWpscan(technologies):

    vulns = []
    patterns = ""
    # Wordpress has 3 main parts for searching
    core = []
    theme = []
    plugin = []

    # Vulns searching for core
    # if (technologies['version']['number'] != None):
    if ('version' in technologies and 'number' in technologies['version']):
        patterns = "wordpress" + " " + "core" + " " + technologies['version']['number']
        results = requestToLocalExploitDB(patterns)
        vulns = vulns + results['RESULTS_EXPLOIT']

    # Vulns searching for themes
    if ('themes' in technologies):

        if (len(technologies['themes'].keys()) == 0):
            vulns = vulns + []
        else:
            for theme in technologies['themes'].keys():
                if (technologies['themes'][theme]['version'] == None):
                    patterns = "wordpress theme" + " " + technologies['themes'][theme]['slug']
                else:
                    patterns = "wordpress theme" + " " + technologies['themes'][theme]['slug'] + " " + technologies['themes'][theme]['version']['number']
                results = requestToLocalExploitDB(patterns)
                vulns = vulns + results['RESULTS_EXPLOIT']

    # Vulns searching for plugins
    if ('plugins' in technologies):
        if (len(technologies['plugins'].keys()) == 0):
            vulns = vulns + []
        else:
            for plugin in technologies['plugins'].keys():
                if (technologies['plugins'][plugin]['version'] == None):
                    patterns = "wordpress plugin" + " " + technologies['plugins'][plugin]['slug']
                else:
                    patterns = "wordpress plugin" + " " + technologies['plugins'][plugin]['slug'] + " " + technologies['plugins'][plugin]['version']['number']
                results = requestToLocalExploitDB(patterns)
                vulns = vulns + results['RESULTS_EXPLOIT']

    return vulns

def getVulnsForJoomscan(technologies):

    vulns = []

    # Parse HTML reports to get version and components info
    versionAndComponentsList = parseReportHTML(technologies)
    print(versionAndComponentsList)
    version = versionAndComponentsList['version']
    components = versionAndComponentsList['components']

    results = requestToLocalExploitDB('joomla ' + version)
    vulns = vulns + results['RESULTS_EXPLOIT']

    for component in components:
        results = requestToLocalExploitDB('joomla component ' + component)
        vulns = vulns + results['RESULTS_EXPLOIT']
    
    return vulns


def getVulnsForDroopescan(technologies):

    vulns = []
    patterns = ""

    # Vulns searching for version
    if ('version' in technologies):
        if (technologies['version']['is_empty'] == False):
            if ('cms_name' in technologies):
                if (technologies['cms_name'] == 'wordpress'):
                    patterns = 'wordpress core ' + technologies['version']['finds'][0]
                    results = requestToLocalExploitDB(patterns)
                    vulns = vulns + results['RESULTS_EXPLOIT']
                else:
                    patterns = technologies['cms_name'] + ' ' + technologies['version']['finds'][0]
                    results = requestToLocalExploitDB(patterns)
                    vulns = vulns + results['RESULTS_EXPLOIT']

    # Vulns searching for plugin
    if ('plugins' in technologies):
        print('get here plugin')
        if (technologies['plugins']['is_empty'] == False):
            if ('cms_name' in technologies):
                if (technologies['cms_name'] == 'wordpress'):
                    patterns = 'wordpress plugin '
                else:
                    patterns = technologies['cms_name'] + ' '
                for find in technologies['plugins']['finds']:
                    patterns = patterns + find['name']
                    results = requestToLocalExploitDB(patterns)
                    vulns = vulns + results['RESULTS_EXPLOIT']
    
    # Vulns searching for theme
    if ('themes' in technologies):
        if (technologies['themes']['is_empty'] == False):
            if ('cms_name' in technologies):
                if (technologies['cms_name'] == 'wordpress'):
                    patterns = 'wordpress theme '
                else:
                    patterns = technologies['cms_name'] + ' '
                for find in technologies['themes']['finds']:
                    patterns = patterns + find['name']
                    results = requestToLocalExploitDB(patterns)
                    vulns = vulns + results['RESULTS_EXPLOIT']

    return vulns

def getVulnsFromExpoitDB(nameOfTool, technologies):

    # If tool is whatweb
    if (nameOfTool == 'whatweb'):
        vulns = getVulnsForWhatWeb(technologies)
        return vulns

    # If tool is webtech
    elif (nameOfTool == 'webtech'):
        vulns = getVulnsForWebTech(technologies)
        return vulns

    elif (nameOfTool == 'nmap'):
        vulns = getVulnsForNmap()
        return vulns
    
    elif (nameOfTool == 'wpscan'):
        vulns = getVulnsForWpscan(technologies)
        return vulns

    elif (nameOfTool == 'joomscan'):
        vulns = getVulnsForJoomscan(technologies)
        return vulns
    
    elif (nameOfTool == 'droopescan'):
        vulns = getVulnsForDroopescan(technologies)
        return vulns

