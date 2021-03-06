import flask
from flask import Response, request, jsonify, send_file
import xml.etree.ElementTree as ET
import re, os, signal
import json, xmltodict, time
import threading
import urllib.request
from pids import pids_of_token

# Update searchsploit tool
from searchsploit_tool.searchsploitUpdate import update

# Screenshot a websitef
from screenshot_tool.screenshot_tool import take_screenshot

# Modules for Exploit DB
from searchsploit_tool.searchsploit_tool import getDataFromSearchsploit
from vulnsfind_tool.vulnsfind_tool import getVulnsFromExpoitDB

# local_modules

# Modules for web technologies scanning
from whatweb_tool.whatweb_tool import getDataFromWhatWeb
from webtech_tool.webtech_tool import getDataFromWebTech

# Modules for subdomains scanning
from sublist3r_tool.sublist3r_tool import getDataFromSublist3r

# Modules for directories/files scanning
from gobuster_tool.gobuster_tool import getDirsFromGobuster, getFilesFromGobuster

# Modules for domain information 
from whois_tool.whois_tool import getDataFromWhois

# Modules which related to DNS
from dig_tool.dig_tool import getDataFromDig
from fierce_tool.fierce_tool import getDataFromFierce

# Modules for Server scanning
from nmap_tool.nmap_tool import getDataFromNmap

# Modules for WAF scanning
from wafw00f_tool.wafw00f_tool import getDataFromWafw00f

# Modules for CMS scanning
from wpscan_tool.wpscan_tool import getDataFromWpscan
from droopescan_tool.droopescan_tool import getDataFromDroopescan
from joomscan_tool.joomscan_tool import getDataFromJoomscan
from cmseek_tool.cmseek_tool import getDataFromCmseek

# Modules Web scanning with Nikto 
from nikto_tool.nikto_tool import getDataFromNikto

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.before_request
def before_request_func():
    try:
        token = request.args['token']
        if (token not in  pids_of_token.keys()):
            pids_of_token[token] = []
    except:
        print("Pass")

# Check whether url is available
@app.route('/api/v1/enumeration/check_available', methods=['GET'])
def check_available():
    try:
        status_code = urllib.request.urlopen(request.args['url'], timeout=60).getcode()
        if (status_code == 200):
            return jsonify('available')
        else:
            return jsonify('unavailable')
    except:
        return jsonify('unavailable')
    
# Web technologies scanning
@app.route('/api/v1/enumeration/whatweb', methods=['GET'])
def whatweb_api():
    if 'url' in request.args:
        #Get cookie if it is defined
        try:
            cookie = request.args['cookie']
        except:
            cookie = None
        results = getDataFromWhatWeb(request.args['url'], cookie, request.args['token'])

        contents = {}
        contents['technologies'] = []
        contents['vulns'] = []

        if (results):

            reportName = 'whatweb_' + request.args['token'] + '.report'
            reportPath = os.path.join( '/root/python_tool/whatweb_tool', reportName)
            
            with open(reportPath, 'r') as f:
                data = xmltodict.parse(f.read())
                
                # In case wrong URL or nothing return
                if (data['log'] == None):
                    return jsonify(contents)
                else:
                    # Delete key:value which un-needed
                    try:
                        # In case having many targets
                        for i in range(0, len(data['log']['target'])):
                            contents['technologies'] = contents['technologies'] + data['log']['target'][i]['plugin']

                        # Remove duplicate technologies
                        res_list = []
                        for i in range(len(contents['technologies'])):
                            if contents['technologies'][i] not in contents['technologies'][i + 1:]:
                                res_list.append(contents['technologies'][i])
                        
                        # Assign res_list back again to contents
                        # Delete element which is not-needed like Title, Country
                        contents['technologies'] = list(filter(lambda element: element['name'] != 'Title' and element['name'] != 'Country' and element['name'] != 'IP', res_list))
                        contents['vulns'] = getVulnsFromExpoitDB('whatweb', contents['technologies'])
                        return jsonify(contents)

                    except: 
                        # In case having only one target
                        contents['technologies'] = list(filter(lambda element: element['name'] != 'Title' and element['name'] != 'Country' and element['name'] != 'IP', data['log']['target']['plugin']))
                        contents['vulns'] = getVulnsFromExpoitDB('whatweb', contents['technologies'])
                        return jsonify(contents)
        else:
            return jsonify(contents)
    else:
        return jsonify('Define url parameter')

@app.route('/api/v1/enumeration/webtech', methods=['GET'])
def webtech_api():
    if 'url' in request.args:
        # Check if URL has http|https
        rightFormat = re.search("^(http|https)://", request.args['url'])

        contents = {}
        contents['technologies'] = []
        contents['vulns'] = []

        if (rightFormat):
            results = getDataFromWebTech(request.args['url'])
            if (results != "Connection Error"):

                # Remove 'tech' key and replace by 'technologies'
                contents['technologies'] = results.pop('tech')
                contents['vulns'] = getVulnsFromExpoitDB('webtech', contents['technologies'])

                return jsonify(contents)
            else:
                return jsonify(contents)
        else:
            return jsonify("Please add 'http' or 'https' to url parameter")
    else:
        return jsonify("Define url parameter")


# Subdomains scanning
@app.route('/api/v1/enumeration/sublist3r', methods=['GET'])
def sublist3r_api():
    if 'url' in request.args:

        results = {}
        results['subdomains'] = []

        subdomains = getDataFromSublist3r(request.args['url'])

        if (len(subdomains) != 0) :
            results = {}
            results['subdomains'] = list(subdomains)
            return jsonify(results)
        else:
            return jsonify(results)
    else:
        return jsonify('Define url parameter')


# Directories/files scanning
@app.route('/api/v1/enumeration/gobuster', methods=['GET'])
def gobuster_api():
    #Check whether requests have url parameter
    if 'url' in request.args:
        
        #Check whether url parameter in right format
        rightFormat = re.search("^(http|https)://", request.args['url'])

        #Get cookie if it is defined
        try:
            cookie = request.args['cookie']
        except:
            cookie = ""

        if (rightFormat):
            results_dirs = getDirsFromGobuster(request.args['url'], cookie, request.args['token'])
            results_files = getFilesFromGobuster(request.args['url'], cookie, request.args['token'])

            results = {}
            results['files'] = []
            results['directories'] = []

            if (results_dirs == 'wrong URL' and results_files == 'wrong URL'):
                return jsonify(results)

            else:
                if (results_dirs != 'wrong URL'):
                    data = []
                    directories = results_dirs.decode('UTF-8').strip().split('\n\r')
                    for directory in directories:
                        data.append(directory.strip())
                    results['directories'] = data

                if (results_files != 'wrong URL'):
                    data = []
                    files = results_files.decode('UTF-8').strip().split('\n\r')
                    for file in files:
                        data.append(file.strip())    
                    results['files'] = data

                return jsonify(results)
        else:
            return jsonify("Please add 'http' or 'https' to url parameter")
    else:
        return jsonify('Define url parameter')


# Domain information
@app.route('/api/v1/enumeration/whois', methods=['GET'])
def whois_api():
    if 'url' in request.args:
        info = getDataFromWhois(request.args['url'])
        return jsonify(info)
    else:
        return jsonify('Define url parameter')


# DNS information
@app.route('/api/v1/enumeration/dig', methods=['GET'])
def dig_api():

    if 'url' in request.args:

        contents = getDataFromDig(request.args['url'])
        # return jsonify(contents)
        return jsonify(contents)

    else:
        return jsonify('Define url parameter')

@app.route('/api/v1/enumeration/fierce', methods=['GET'])
def fierce_api():

    if 'url' in request.args:

        contents = getDataFromFierce(request.args['url'], request.args['token'])

        reportName = 'fierce_' + request.args['token'] + '.report'
        reportPath = os.path.join('/root/python_tool/fierce', reportName)

        try:
            with open(reportPath,'r') as f:
                return jsonify(f.read())
        except:
            return jsonify('')

    else:
        return jsonify('Define url parameter')


# Server information
@app.route('/api/v1/enumeration/nmap', methods=['GET'])
def nmap_api():
    if 'url' in request.args:
        results = getDataFromNmap(request.args['url'], request.args['token'])

        contents = {}
        contents['nmap'] = ''
        contents['vulns'] = []

        reportNameTXT = 'nmap_' + request.args['token'] + '.report_1'
        reportNameXML = 'nmap_' + request.args['token'] + '.report_2'

        reportPathTXT = os.path.join('/root/python_tool/nmap_tool', reportNameTXT)
        reportPathXML = os.path.join('/root/python_tool/nmap_tool', reportNameXML)

        if (results != "Can not get data from nmap"):
            with open(reportPathTXT,'r') as f:
                # Load to dictionary again for post-processing
                contents['nmap'] = f.read()   
                contents['vulns'] = getVulnsFromExpoitDB(reportPathXML,[])
                return contents
        else:
            return contents
    else:
        return jsonify('Define url parameter')


# WAF scanning
@app.route('/api/v1/enumeration/wafw00f', methods=['GET'])
def wafw00f_api():
    if 'url' in request.args:
        results = getDataFromWafw00f(request.args['url'], request.args['token'])

        contents = {}
        contents['wafs'] = []

        if (results):

            reportName = 'wafw00f_' + request.args['token'] + '.report'
            reportPath = os.path.join('/root/python_tool/wafw00f_tool', reportName)

            with open(reportPath,'r') as f:
                tmp = json.loads(f.read())
                contents['wafs'] = tmp
                return jsonify(contents)
        else:
            return jsonify(contents)
    else:
        return jsonify('Define url parameter') 


# CMS scanning
@app.route('/api/v1/enumeration/wpscan', methods=['GET'])
def wpscan_api():
    if 'url' in request.args:

        #Check whether url parameter in right format
        rightFormat = re.search("^(http|https)://", request.args['url'])

        contents = {}
        
        if (rightFormat):

            #Get cookie if it is defined
            try:
                cookie = request.args['cookie']
            except:
                cookie = None

            results = getDataFromWpscan(request.args['url'], cookie, request.args['token'])

            reportName = 'wpscan_' + request.args['token'] + '.report'
            reportPath = os.path.join('/root/python_tool/wpscan_tool', reportName)

            if (results):
                with open(reportPath, 'r') as f:
                    contents = json.loads(f.read())
                    contents['vulns'] = getVulnsFromExpoitDB('wpscan', contents)
                    return jsonify(contents)
            else:
                contents['vulns'] = []
                return jsonify(contents)
        else:
            return jsonify("Please add 'http' or 'https' to url parameter")
    else:
        return jsonify('Define url paramter')

@app.route('/api/v1/enumeration/droopescan', methods=['GET'])
def droopescan_api():
    if 'url' in request.args:

        results = getDataFromDroopescan(request.args['url'], request.args['token'])
        
        contents = {}
        contents['droopescan'] = {}
        contents['vulns'] = []

        if (results != "Can not get data from droopescan"):
            try:
                contents['droopescan'] = json.loads(results.decode('utf-8'))
                # contents['droopescan'] = results.decode('utf-8')
                contents['vulns'] = getVulnsFromExpoitDB('droopescan',contents['droopescan'])
                return contents
            except:
                return jsonify(contents)
        else:
            return jsonify(contents)
    else:
        return jsonify('Define url paramter')

@app.route('/api/v1/enumeration/joomscan', methods=['GET'])
def joomscan_api():
    if 'url' in request.args:

        results = getDataFromJoomscan(request.args['url'], request.args['token'])

        contents = {}
        contents['joomscan'] = ""
        contents['vulns'] = []

        if (results):
            # Get path of reports
            path = '/root/python_tool/joomscan/reports/'
            try:
                reportFolder = os.listdir(path)[0]
                reportPath = os.path.join(path, reportFolder)
            except:
                return contents

            # Read contents in report with extension is txt
            for reportFile in os.listdir(reportPath):
                if re.search("(.txt)$", reportFile):

                    with open(os.path.join(reportPath, reportFile), 'r') as f:
                        contents['joomscan'] = f.read()
                else:
                    with open(os.path.join(reportPath, reportFile), 'r') as f:
                       contents['vulns'] = getVulnsFromExpoitDB('joomscan',f.read())    

            return contents

        else:
            return contents
    
    else:
        return jsonify('Define url paramter')

@app.route('/api/v1/enumeration/cmseek', methods=['GET'])
def cmseek_api():
    if 'url' in request.args:
        # request.args['url'] auto decode
        results, reportPath = getDataFromCmseek(request.args['url'], request.args['token'])
        if (results != "Can not get data from cmseek"):

            with open(f"{reportPath}/cms.json",'r') as f:
                contents = json.loads(f.read())
                return contents
        else:
            return {
                "cms_id": "", 
                "cms_name": "", 
                "cms_url": "", 
                "detection_param": "",
            }
    else:
        return jsonify('Define url paramter')
    
# Web scanning with Nikto      
@app.route('/api/v1/enumeration/nikto', methods=['GET'])  
def nikto_api():
    if 'url' in request.args:
        rightFormat = re.search("^(http|https)://", request.args['url'])

        contents = {}

        if (rightFormat):
            results = getDataFromNikto(request.args['url'], request.args['token'])
            if (results):

                reportName = 'nikto_' + request.args['token'] + '.report' 
                reportPath = os.path.join('/root/python_tool/nikto_tool/', reportName)

                with open(reportPath, 'r') as f:
                    fileContent = f.read()
                    try:
                        contents = json.loads(fileContent[::-1].replace(',','',2)[::-1])
                        return jsonify(contents)
                    except:
                        try:
                            contents = json.loads(fileContent[::-1].replace(',','',1).replace('}','',1)[::-1])
                            return jsonify(contents)
                        except:
                            try:
                                contents = json.loads(fileContent.replace('}','',1))
                                return jsonify(contents)
                            except:
                                return jsonify({})           
            else:
                return jsonify(contents)
        else:
            return jsonify("Please add 'http' or 'https' to url parameter")
    else:
        return jsonify('Define url paramter')

# Search exploit from ExploitDB
@app.route('/api/v1/enumeration/searchsploit', methods=['GET'])
def searchsploit_api():

    path = 'https://www.exploit-db.com/raw/'

    if 'pattern' in request.args:
        results = getDataFromSearchsploit(request.args['pattern'])
        contents = {}
        contents['RESULTS_EXPLOIT'] = []

        if (results != "Error"):
            # Process byte array data from tool
            results = results.decode('UTF-8').replace('\n\n\n','\n').replace('\n\t\t','').replace('\n\t','').replace('\t','')
            results = re.sub(r']\n}',']}', results)
            results = results.split('\n')

            for index in range(len(results) - 1):
                try:
                    result = json.loads(results[index])
                except:
                    return contents

                for pos in range(len(result['RESULTS_EXPLOIT'])):
                    edb_id = result['RESULTS_EXPLOIT'][pos]['EDB-ID']
                    result['RESULTS_EXPLOIT'][pos]['Path'] = path + edb_id
                
                contents['RESULTS_EXPLOIT'] = contents['RESULTS_EXPLOIT'] + result['RESULTS_EXPLOIT']

            return jsonify(contents)
        else:
            return jsonify(contents)
    else:
        return jsonify('Define url paramter')

@app.route('/api/v1/enumeration/screenshot', methods=['GET'])
def screenshot_api():
    if 'url' in request.args:
        right_format = re.search('^(http|https)://', request.args['url'])
        if (right_format):
            try:
                PATH = '/root/python_tool/screenshot_tool/'
                image_file = PATH + request.args['token'] + '.png'
                take_screenshot(request.args['url'], request.args['token'])
                return send_file(image_file, mimetype='image/png')
            except:
                return jsonify("No picture")
        else:
            return jsonify("Please add 'http' or 'https' to url parameter")
    return jsonify('Define url paramter')

@app.route('/api/v1/enumeration/stop_all_tools', methods=['GET'])
def kill_all_process():
    token = request.args['token']

    # Wait all tools have gone to api-server
    time.sleep(15)

    if (token in pids_of_token.keys()):
        for pid in pids_of_token[token]:
            # Kill each tool related to token
            os.kill(pid, signal.SIGKILL)
        # Delete token out of pids_of_token
        del pids_of_token[token]

    return jsonify("OK")

if __name__ == "__main__":
    threading.Thread(target=update, args=()).start()
    app.run(host='0.0.0.0', port=5000)